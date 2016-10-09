#!/usr/bin/env python
# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

import argparse
from collections import namedtuple
import itertools
import json
import os.path
import platform
import re
import shutil
import sys

import dataproperty
import logbook
import six
import subprocrunner


handler = logbook.StderrHandler()
handler.push_application()

logger = logbook.Logger(os.path.splitext(os.path.basename(__file__))[0])

DEFAULT_CMAKE_OPTIONS_FILE = "cmake_options.json"


class BuildAction(object):
    CMAKE = "cmake"
    RECMAKE = "recmake"
    CLEAN = "clean"
    BUILD = "build"
    REBUILD = "rebuild"

    DEFAULT = BUILD
    LIST = [CMAKE, RECMAKE, CLEAN, BUILD, REBUILD]


class BuildType(object):
    DEBUG = "Debug"
    RELEASE = "Release"

    DEFAULT = DEBUG
    LIST = [DEBUG, RELEASE]


def parse_option():
    description = "CMake wrapper"
    epilog = ""
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=description, epilog=epilog)

    group = parser.add_argument_group("Directory Options")
    group.add_argument(
        "--test-dir", default="test",
        help="""
        relative path to the test case directory
        (defaults to '%(default)s').
        """)
    group.add_argument(
        "--build-dir", default="build",
        help="""
        relative path to the build output directory
        (defaults to '%(default)s').
        """)

    group = parser.add_argument_group("Build Options")
    group.add_argument(
        "--action", choices=BuildAction.LIST, default=BuildAction.DEFAULT,
        help="""
        cmake: execute CMake and exit.
        clean: delete existing build directory and exit.
        recmake: delete existing CMakeCache and execute CMake after that.
        build: execute MSBuild to Visual Studio solution files that created by cmake.
        rebuild: delete existing build directory and execute CMake and MSBuild after that.
        defaults to '%(default)s'.
        """)

    group = parser.add_argument_group("CMake Options")
    group.add_argument(
        "--cmake-options",
        default=DEFAULT_CMAKE_OPTIONS_FILE,
        help="""
        path to the CMake options file. use "{key :value, ...}"
        to set specific parameters. defaults to %(default)s.
        """)
    group.add_argument(
        "--build-type", choices=BuildType.LIST, default=BuildType.DEFAULT,
        help="defaults to %(default)s.")
    group.add_argument(
        "--generator",
        help="""
        generator that pass to cmake.
        gtestmake automatically make generator 'Visual Studio NN [arch]' and
        pass to cmake if:
        (1) executed on Windows platform.
        (2) executed without --generator option.
        (3) Visual Studio is installed in C: or D: drive.
        """)

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--debug", dest="log_level", action="store_const",
        const=logbook.DEBUG, default=logbook.INFO,
        help="for debug print.")
    group.add_argument(
        "--quiet", action="store_true", default=False,
        help="suppress execution log messages.")

    return parser.parse_args()


class VisualStudioInfo(object):
    __RE_VS_DIR_NAME = re.compile("Microsoft Visual Studio [0-9]+[\.][0-9]+")
    __RE_VS_VERSION = re.compile("[0-9]+[\.][0-9]+")

    VersionInfo = namedtuple("VersionInfo", "major minor")

    @property
    def version_info(self):
        return self.__max_version_info

    @property
    def msbuild_path(self):
        return self.__msbuild_path

    def __init__(self, search_drive_list=["C:"]):
        self.__version_info_set = set()
        self.__max_version_info = None
        self.__msbuild_path = None

        if platform.system() != "Windows":
            return

        self.__program_files_dir_list = [
            "Program Files",
            "Program Files (x86)",
        ]

        self.__detect_version(search_drive_list)
        self.__detect_msbuild(search_drive_list)

    def __detect_version(self, search_drive_list):
        max_vs_version = 0

        for search_drive, program_files_dir in itertools.product(
                search_drive_list, self.__program_files_dir_list):

            try:
                dir_list = os.listdir(
                    "{:s}\\{:s}".format(search_drive, program_files_dir))
            except WindowsError:
                continue

            for dir_name in dir_list:
                match = self.__RE_VS_DIR_NAME.search(dir_name)
                if match is None:
                    continue

                version_string = self.__RE_VS_VERSION.search(
                    match.group()).group()
                vs_version = float(version_string)
                version_info = self.VersionInfo(*[
                    int(ver) for ver in version_string.split(".")])
                self.__version_info_set.add(version_info)

                if vs_version > max_vs_version:
                    max_vs_version = vs_version
                    self.__max_version_info = version_info

    def __detect_msbuild(self, search_drive_list):
        for search_drive, program_files_dir in itertools.product(
                search_drive_list, self.__program_files_dir_list):

            try:
                dir_list = os.listdir(
                    "{:s}\\{:s}".format(search_drive, program_files_dir))
            except WindowsError:
                continue

            for dir_name in dir_list:
                if dir_name != "MSBuild":
                    continue

                for version_info in reversed(sorted(self.__version_info_set)):
                    msbuild_path = "/".join([
                        search_drive,
                        program_files_dir,
                        dir_name,
                        "{:d}.{:d}".format(
                            version_info.major, version_info.minor),
                        "Bin",
                        "MSBuild.exe",
                    ])

                    if os.path.isfile(msbuild_path):
                        self.__msbuild_path = msbuild_path
                        return

        #raise OSError("MSBuild not found")

_vsinfo = VisualStudioInfo()


class CMakeCommandBuilder(object):

    def __init__(self, options):
        self.__options = options

    def get_cmake_commmand(self, build_dir):
        cmake_command_list = [
            'cd {:s} && cmake ../{:s}'.format(
                build_dir, self.__options.test_dir),
            "-DCMAKE_BUILD_TYPE={:s}".format(self.__options.build_type),
        ]

        for key, value in six.iteritems(self.__read_cmake_options()):
            cmake_command_list.append('{}={}'.format(key, value))

        generator = self.__get_generator()
        if generator is not None:
            cmake_command_list.append('-G "{:s}"'.format(
                generator))

        return " ".join(cmake_command_list)

    @staticmethod
    def __get_win_generator():
        return "Visual Studio {:d} {:s}".format(
            _vsinfo.version_info.major,
            "Win64" if platform.architecture()[0] == "64bit" else ""
        )

    def __get_generator(self):
        generator = None
        if all([
            platform.system() == "Windows",
            self.__options.generator is None,
        ]):
            generator = self.__get_win_generator()

        return generator

    def __read_cmake_options(self):
        file_path = self.__options.cmake_options

        if dataproperty.is_empty_string(file_path):
            return {}

        if not os.path.isfile(file_path):
            return {}

        cmake_options = {}
        with open(file_path) as f:
            cmake_options = json.loads(f.read())

        return cmake_options


def is_root_dir_path(dir_path):
    if platform.system() == "Windows":
        if re.search(r"^[a-zA-Z]:\\?$", dir_path) is not None:
            return True

    return dir_path == "/"


def clean(build_dir_path):
    if dataproperty.is_empty_string(build_dir_path):
        return 0

    if is_root_dir_path(build_dir_path):
        return 1

    logger.debug('delete "{:s}" directory'.format(build_dir_path))
    shutil.rmtree(build_dir_path, ignore_errors=True)

    return 0


def find_solution_file_list(root_path):
    re_solution = re.compile("[\.]sln$")
    solution_file_path_list = []

    for filename in os.listdir(root_path):
        if re_solution.search(filename) is None:
            continue

        solution_file_path_list.append("/".join([root_path, filename]))

    return solution_file_path_list


def build(build_dir):
    for solution_file in find_solution_file_list(build_dir):
        build_command = '"{:s}" {:s}'.format(
            _vsinfo.msbuild_path, solution_file)

        runner = subprocrunner.SubprocessRunner(build_command)
        runner.run()
        logger.info(runner.stdout)
        if dataproperty.is_not_empty_string(runner.stderr):
            logger.error(runner.stderr)


def main():
    options = parse_option()

    logger.level = options.log_level
    subprocrunner.logger.level = options.log_level
    if options.quiet:
        logger.disable()
        subprocrunner.logger.disable()
    else:
        logger.enable()
        subprocrunner.logger.enable()

    build_dir = options.build_dir
    if options.action in [BuildAction.CLEAN, BuildAction.REBUILD]:
        result = clean(build_dir)
        return result

    if options.action in [BuildAction.RECMAKE]:
        cmake_cache_path = "/".join([build_dir, "CMakeCache.txt"])
        logger.debug("delete {:s}".format(cmake_cache_path))
        os.remove(cmake_cache_path)

    if not os.path.isdir(build_dir):
        os.makedirs(build_dir)

    if options.action in [
            BuildAction.CMAKE, BuildAction.RECMAKE,
            BuildAction.BUILD, BuildAction.REBUILD]:
        command_builder = CMakeCommandBuilder(options)
        runner = subprocrunner.SubprocessRunner(
            command_builder.get_cmake_commmand(build_dir))
        runner.run()
        logger.info(runner.stdout)
        logger.info(runner.stderr)

    if options.action in [BuildAction.BUILD, BuildAction.REBUILD]:
        build(build_dir)

    return 0

if __name__ == '__main__':
    sys.exit(main())
