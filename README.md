# gtest-project-template
Test template project of [Google Test](https://github.com/google/googletest) for C++.

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
pip install cmakew --upgrade
```


## Example
### Environment
- Windows 64-bit
    - Command Prompt
- Visual Studio 2015
- Python 2.7.12

### Execute CMake
```
gtest-project-template> cmakew test
```



# Dependency
## Mandatory
- [googletest](https://github.com/google/googletest.git)
- [cmake](https://cmake.org/download/)

## Optional
- [Python](https://www.python.org/)

### Optional Python packages
- [cmakew](https://github.com/thombashi/cmakew)
