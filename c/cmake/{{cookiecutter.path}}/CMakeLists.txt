cmake_minimum_required(VERSION 3.14...3.25)

project(
  {{cookiecutter.path}}
  VERSION 0.1
  DESCRIPTION "Add description"
  LANGUAGES C)

if(CMAKE_PROJECT_NAME STREQUAL PROJECT_NAME)
    # Optionally set things like CMAKE_C_STANDARD, CMAKE_POSITION_INDEPENDENT_CODE here
    set(CMAKE_C_STANDARD 17)
    set(CMAKE_C_STANDARD_REQUIRED ON)

    # Let's ensure -std=cxx instead of -std=gxx
    set(CMAKE_C_EXTENSIONS OFF)

    # Let's nicely support folders in IDEs
    set_property(GLOBAL PROPERTY USE_FOLDERS ON)
endif()

add_subdirectory(src)
