# gtest-project-template
C++ test project template using [Google Test](https://github.com/google/googletest).

## Included
- Google Test
    - [Google Test](https://github.com/google/googletest) 1.8.0 (as a submodule)
    - Basic test case templates
    - Basic Google Test fixtures
- CMake
    - ``CMakeLists.txt``


# Installation
```
git clone https://github.com/thombashi/gtest-project-template.git --recursive
```


## CMake/Compiler wrapper tool (optional)
[cmakew](https://github.com/thombashi/cmakew)

```
pip install cmakew --upgrade
```


## Usage
### Environment
- Fedora 24
- gcc-c++ 6.3.1
- Python 3.6.1

### Build test cases
```
$ cd gtest-project-template
$ cp -ar test_template/ test/
Written test cases
$ cmakew test
```


# Dependency
## Mandatory
- [googletest](https://github.com/google/googletest.git)
- [cmake](https://cmake.org/download/)
- Compiler: ``Visual Studio``, ``gcc``, etc.
