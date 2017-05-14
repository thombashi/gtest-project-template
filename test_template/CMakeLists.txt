cmake_minimum_required(VERSION 3.0.2)

set(PROJECT_NAME gtest_project_template)  # todo: rename project
project(${PROJECT_NAME} CXX)


message("- build flags ----------------------------------------")
if(${CMAKE_GENERATOR} MATCHES "Visual Studio [0-9]+")
    message(${CMAKE_GENERATOR})

    set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} /MT")
    set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} /MTd")
else()
    set(CMAKE_CXX_FLAGS "-std=c++11")
endif()


message("- paths ----------------------------------------")
get_filename_component(TEST_ROOT . ABSOLUTE)
get_filename_component(WORKSPACE_ROOT ${TEST_ROOT}/.. ABSOLUTE)
set(UTILS_DIR ${TEST_ROOT}/utils)
set(FIXTURE_DIR ${TEST_ROOT}/fixture)

message("CMAKE_BUILD_TYPE: ${CMAKE_BUILD_TYPE}")
message("PROJECT_BINARY_DIR: ${PROJECT_BINARY_DIR}")

message("TEST_ROOT: ${TEST_ROOT}")
message("WORKSPACE_ROOT: ${WORKSPACE_ROOT}")
message("UTILS_DIR: ${UTILS_DIR}")
message("FIXTURE_DIR: ${FIXTURE_DIR}")

# includes ---
set(INCLUDES
    ${UTILS_DIR}
    ${FIXTURE_DIR}
)

message("INCLUDES: ${INCLUDES}")
include_directories(${INCLUDES})

# sources ---
# file(GLOB UTILS_CPP ${UTILS_DIR}/*.cpp)
file(GLOB FIXTURE_CPP ${FIXTURE_DIR}/*.cpp)
set(SOURCES
    # ${UTILS_CPP}
    ${FIXTURE_CPP}
)

message("SOURCES: ${SOURCES}")


message("- gtest ----------------------------------------")
enable_testing()

#set(BUILD_GTEST ON CACHE BOOL "Build Google Test library")
#set(BUILD_GMOCK OFF CACHE BOOL "Build Google Mock library")
add_subdirectory(gtest)

#message("- aws-sdk-cpp ----------------------------------------")
#find_package(aws-sdk-cpp)

#add_definitions(-DUSE_IMPORT_EXPORT)

message("- libraries ----------------------------------------")
set(LIBS
    gtest
    gtest_main
)

message("LIBS: ${LIBS}")


message("- test ----------------------------------------")

# todo: add/delete tests
set(TEST_LIST
    test_template
    test_template_param
    test_template_combine_param
)

foreach(TEST_NAME ${TEST_LIST})
    message("add executable: ${TEST_NAME}")
    set(EXEC_NAME ${TEST_NAME})

    # todo: add/delete sources
    add_executable(${EXEC_NAME}
        ${TEST_NAME}.cpp
        ${SOURCES}
    )
    set_property(TARGET ${EXEC_NAME} PROPERTY CXX_STANDARD 11)
    set_property(TARGET ${EXEC_NAME} PROPERTY CXX_STANDARD_REQUIRED ON)

    target_link_libraries(${EXEC_NAME} ${LIBS})
    add_test(
        NAME ${EXEC_NAME}
        COMMAND $<TARGET_FILE:${EXEC_NAME}>
    )
endforeach(TEST_NAME)
