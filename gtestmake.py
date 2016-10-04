#!/usr/bin/env python
# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

import argparse
import itertools
import os.path
import platform
import re
import sys
import shutil

import dataproperty
import logbook
import subprocrunner

handler = logbook.StderrHandler()
handler.push_application()

logger = logbook.Logger(os.path.splitext(os.path.basename(__file__))[0])


def parse_option():
    description = "CMake wrapper"
    epilog = ""
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=description, epilog=epilog)

    group = parser.add_argument_group("Directory Options")
    group.add_argument(
        "--clean", action="store_true", default=False,
        help="delete build directory and exit.")
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


def get_win_generator():
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


def get_cmake_commmand(build_dir, options):
    generator = None
    if all([
        platform.system() == "Windows",
        options.generator is None,
    ]):
        generator = get_win_generator()

    command_list = [
        'cd {:s} && cmake ../{:s}'.format(build_dir, options.test_dir)
    ]
    if generator is not None:
        command_list.append('-G "{:s}"'.format(
            generator))

    return " ".join(command_list)


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
    if options.clean:
        return clean(build_dir)

    os.makedirs(build_dir)
    runner = subprocrunner.SubprocessRunner(
        get_cmake_commmand(build_dir, options))
    runner.run()
    logger.info(runner.stdout)

    return 0

if __name__ == '__main__':
    sys.exit(main())
