# gtest-project-template
Test templete project of [Google Test](https://github.com/google/googletest).

## Included
- Google Test
    - Google Test 1.8.0 (as submodule)
    - Basic Google Test fixtures
    - Basic test templates
- CMake
    - CMakeLists.txt
    - CMake wrapper script (optional)


# Installation
```
git clone https://github.com/thombashi/gtest-project-template.git --recursive
```


# CMake wrapper (optional)
`gtestmake.py` is a CMake wrapper script for Google Test.

## Installation
```
pip install --upgrade subprocrunner
```

- Note: required [Python](https://www.python.org/) 2.7+ or 3.3+


## help
```
usage: gtestmake.py [-h] [--clean] [--test-dir TEST_DIR]
                    [--build-dir BUILD_DIR] [--generator GENERATOR]
                    [--debug | --quiet]

optional arguments:
  -h, --help            show this help message and exit
  --debug               for debug print.
  --quiet               suppress execution log messages.

Directory Options:
  --clean               delete build directory and exit.
  --test-dir TEST_DIR   relative path to the test case directory (defaults to
                        'test').
  --build-dir BUILD_DIR
                        relative path to the build output directory (defaults
                        to 'build').

Build Options:
  --generator GENERATOR
                        generator that pass to cmake. gtestmake automatically
                        make generator 'Visual Studio NN [arch]' and pass to
                        cmake if: (1) executed on Windows platform. (2)
                        executed without --generator option. (3) Visual Studio
                        is installed in C: or D: drive.
```

## Example
### Environment
- Windows 64-bit
    - Command Prompt
- Visual Studio 2015
- Python 2.7.12

### Execute CMake
```
>python gtestmake.py
[2016-10-02 12:24:34.461000] INFO: gtestmake: -- The C compiler identification is MSVC 19.0.24215.1
-- The CXX compiler identification is MSVC 19.0.24215.1
-- Check for working C compiler: C:/Program Files (x86)/Microsoft Visual Studio 14.0/VC/bin/x86_amd64/cl.exe
-- Check for working C compiler: C:/Program Files (x86)/Microsoft Visual Studio 14.0/VC/bin/x86_amd64/cl.exe -- works
-- Detecting C compiler ABI info
-- Detecting C compiler ABI info - done
-- Check for working CXX compiler: C:/Program Files (x86)/Microsoft Visual Studio 14.0/VC/bin/x86_amd64/cl.exe
-- Check for working CXX compiler: C:/Program Files (x86)/Microsoft Visual Studio 14.0/VC/bin/x86_amd64/cl.exe -- works
-- Detecting CXX compiler ABI info
-- Detecting CXX compiler ABI info - done
-- Detecting CXX compile features
-- Detecting CXX compile features - done
-- Found PythonInterp: C:/Python27/python.exe (found version "2.7.12")
-- Looking for pthread.h
-- Looking for pthread.h - not found
-- Found Threads: TRUE
-- Configuring done
-- Generating done
-- Build files have been written to: C:/Users/dev/workspace/gtest-project-template/build
```

### Delete build outputs
```
>python gtestmake.py --clean
```


# Dependency
## Mandatory
- [googletest](https://github.com/google/googletest.git)
- [cmake](https://cmake.org/download/)

## Optional
- [Python](https://www.python.org/)

### Optional Python packages
- [subprocrunner](https://github.com/thombashi/subprocrunner)
