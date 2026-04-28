# Install script for directory: /home/lmz/gr-radar/include/radar

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

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/radar" TYPE FILE FILES
    "/home/lmz/gr-radar/include/radar/api.h"
    "/home/lmz/gr-radar/include/radar/signal_generator_cw_c.h"
    "/home/lmz/gr-radar/include/radar/signal_generator_fmcw_c.h"
    "/home/lmz/gr-radar/include/radar/split_cc.h"
    "/home/lmz/gr-radar/include/radar/os_cfar_c.h"
    "/home/lmz/gr-radar/include/radar/ts_fft_cc.h"
    "/home/lmz/gr-radar/include/radar/estimator_cw.h"
    "/home/lmz/gr-radar/include/radar/print_results.h"
    "/home/lmz/gr-radar/include/radar/static_target_simulator_cc.h"
    "/home/lmz/gr-radar/include/radar/signal_generator_fsk_c.h"
    "/home/lmz/gr-radar/include/radar/split_fsk_cc.h"
    "/home/lmz/gr-radar/include/radar/estimator_fsk.h"
    "/home/lmz/gr-radar/include/radar/usrp_echotimer_cc.h"
    "/home/lmz/gr-radar/include/radar/estimator_fmcw.h"
    "/home/lmz/gr-radar/include/radar/signal_generator_sync_pulse_c.h"
    "/home/lmz/gr-radar/include/radar/estimator_sync_pulse_c.h"
    "/home/lmz/gr-radar/include/radar/find_max_peak_c.h"
    "/home/lmz/gr-radar/include/radar/qtgui_scatter_plot.h"
    "/home/lmz/gr-radar/include/radar/qtgui_time_plot.h"
    "/home/lmz/gr-radar/include/radar/tracking_singletarget.h"
    "/home/lmz/gr-radar/include/radar/msg_gate.h"
    "/home/lmz/gr-radar/include/radar/msg_manipulator.h"
    "/home/lmz/gr-radar/include/radar/ofdm_cyclic_prefix_remover_cvc.h"
    "/home/lmz/gr-radar/include/radar/transpose_matrix_vcvc.h"
    "/home/lmz/gr-radar/include/radar/qtgui_spectrogram_plot.h"
    "/home/lmz/gr-radar/include/radar/crop_matrix_vcvc.h"
    "/home/lmz/gr-radar/include/radar/ofdm_divide_vcvc.h"
    "/home/lmz/gr-radar/include/radar/os_cfar_2d_vc.h"
    "/home/lmz/gr-radar/include/radar/estimator_ofdm.h"
    "/home/lmz/gr-radar/include/radar/estimator_rcs.h"
    "/home/lmz/gr-radar/include/radar/trigger_command.h"
    )
endif()

