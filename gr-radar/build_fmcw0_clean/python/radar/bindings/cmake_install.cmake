# Install script for directory: /home/lmz/gr-radar/python/radar/bindings

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/lmz/miniconda3/envs/gr310_fmcw_0")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "Release")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

# Set default install directory permissions.
if(NOT DEFINED CMAKE_OBJDUMP)
  set(CMAKE_OBJDUMP "/usr/bin/objdump")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "pythonapi" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/python3.12/site-packages/gnuradio/radar/radar_python.cpython-312-x86_64-linux-gnu.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/python3.12/site-packages/gnuradio/radar/radar_python.cpython-312-x86_64-linux-gnu.so")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/python3.12/site-packages/gnuradio/radar/radar_python.cpython-312-x86_64-linux-gnu.so"
         RPATH "/home/lmz/miniconda3/envs/gr310_fmcw_0/lib:/usr/lib:/lib")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python3.12/site-packages/gnuradio/radar" TYPE MODULE FILES "/home/lmz/gr-radar/build_fmcw0_clean/python/radar/bindings/radar_python.cpython-312-x86_64-linux-gnu.so")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/python3.12/site-packages/gnuradio/radar/radar_python.cpython-312-x86_64-linux-gnu.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/python3.12/site-packages/gnuradio/radar/radar_python.cpython-312-x86_64-linux-gnu.so")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/python3.12/site-packages/gnuradio/radar/radar_python.cpython-312-x86_64-linux-gnu.so"
         OLD_RPATH "/home/lmz/miniconda3/envs/gr310_fmcw_0/lib:/usr/lib:/lib:/home/lmz/gr-radar/build_fmcw0_clean/lib:"
         NEW_RPATH "/home/lmz/miniconda3/envs/gr310_fmcw_0/lib:/usr/lib:/lib")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/python3.12/site-packages/gnuradio/radar/radar_python.cpython-312-x86_64-linux-gnu.so")
    endif()
  endif()
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "pythonapi" OR NOT CMAKE_INSTALL_COMPONENT)
  include("/home/lmz/gr-radar/build_fmcw0_clean/python/radar/bindings/CMakeFiles/radar_python.dir/install-cxx-module-bmi-Release.cmake" OPTIONAL)
endif()

