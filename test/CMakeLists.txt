cmake_minimum_required(VERSION 3.0)

set(PROJECT_NAME gtest_project_template)  # todo: rename project
project(${PROJECT_NAME})


message("- build flags ----------------------------------------")
if(${CMAKE_GENERATOR} MATCHES "Visual Studio [0-9]+")
	message(${CMAKE_GENERATOR})

	set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} /MT")
	set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} /MTd")
endif()


message("- paths ----------------------------------------")
set(WORKSPACE_ROOT ..)
message("WORKSPACE_ROOT: ${WORKSPACE_ROOT}")


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
        fixture_template.cpp
    )

    target_link_libraries(${EXEC_NAME} ${LIBS})
    add_test(
        NAME ${EXEC_NAME}
        COMMAND $<TARGET_FILE:${EXEC_NAME}>
    )
endforeach(TEST_NAME)
