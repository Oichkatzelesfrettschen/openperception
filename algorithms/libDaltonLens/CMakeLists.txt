cmake_minimum_required(VERSION 3.16)

project(libDaltonLens)

add_definitions(-DTEST_IMAGES_DIR="${CMAKE_SOURCE_DIR}/tests/images/")

# Build the library itself with strict warning flags applied to our source only.
add_library(daltonlens_obj OBJECT libDaltonLens.c libDaltonLens.h)
target_include_directories(daltonlens_obj PUBLIC ${CMAKE_SOURCE_DIR})
if (UNIX)
    target_compile_options(daltonlens_obj PRIVATE -Wall -Wextra -Werror -pedantic)
endif()

# Can't believe I had to go through that, but test aren't built automatically by cmake,
# so we need a special dependency hack. See https://stackoverflow.com/a/10824578
function (add_dl_test)
    add_test (NAME "${ARGV0}_BUILD" COMMAND "${CMAKE_COMMAND}" --build ${CMAKE_BINARY_DIR} --target "${ARGV0}" "--config" "$<CONFIG>" )
    add_test ("${ARGV0}" "${ARGV0}")
    add_executable("${ARGV0}"
        "tests/${ARGV0}.c"
        $<TARGET_OBJECTS:daltonlens_obj>
    )
    # Treat the tests/ directory as a system include so vendored stb headers
    # do not trigger -Wextra/-Werror on code we do not own.
    target_include_directories("${ARGV0}" SYSTEM PRIVATE ${CMAKE_SOURCE_DIR}/tests)
    target_include_directories("${ARGV0}" PRIVATE ${CMAKE_SOURCE_DIR})
    # GCC 15 emits -Wstringop-overflow for a false positive inside stb_image.h
    # (tc[3] array bounds analysis). Suppress only for the test target, not our lib.
    if (CMAKE_C_COMPILER_ID STREQUAL "GNU")
        target_compile_options("${ARGV0}" PRIVATE -Wno-stringop-overflow)
    endif()
    set_tests_properties("${ARGV0}" PROPERTIES DEPENDS "${ARGV0}_BUILD")
    # Common lib for all tests.
    if (UNIX)
        target_link_libraries("${ARGV0}" m)
    endif()
endfunction()

add_dl_test (test_simulation)
enable_testing()
