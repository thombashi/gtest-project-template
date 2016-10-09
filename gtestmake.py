#!/usr/bin/env python
# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

import argparse
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

    DEFAULT = CMAKE
    LIST = [CMAKE, RECMAKE, CLEAN]


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
        recmake: delete existing build directory and execute CMake after that.
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
        re_vs = re.compile("Microsoft Visual Studio [0-9]+[\.][0-9]+")
        re_vs_version = re.compile("[0-9]+")

        search_drive_list = [
            "C:",
            "D:",
        ]
        program_files_dir_list = [
            "Program Files",
            "Program Files (x86)",
        ]
        vs_version = 0

        for search_drive, program_files_dir in itertools.product(
                search_drive_list, program_files_dir_list):

            try:
                dir_list = os.listdir(
                    "{:s}\\{:s}".format(search_drive, program_files_dir))
            except WindowsError:
                continue

            for dir_name in dir_list:
                match = re_vs.search(dir_name)
                if match is None:
                    continue

                vs_version = max(
                    vs_version, int(re_vs_version.search(match.group()).group()))

        generator = "Visual Studio {:d} {:s}".format(
            vs_version,
            "Win64" if platform.architecture()[0] == "64bit" else ""
        )

        return generator

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
    if options.action in [BuildAction.CLEAN, BuildAction.RECMAKE]:
        result = clean(build_dir)
        if options.action == BuildAction.CLEAN:
            return result

    if not os.path.isdir(build_dir):
        os.makedirs(build_dir)

    if options.action in [BuildAction.CMAKE, BuildAction.RECMAKE]:
        command_builder = CMakeCommandBuilder(options)
        runner = subprocrunner.SubprocessRunner(
            command_builder.get_cmake_commmand(build_dir))
        runner.run()
        logger.info(runner.stdout)
        logger.info(runner.stderr)

    return 0

if __name__ == '__main__':
    sys.exit(main())
