# Install script for directory: /home/lmz/gr-radar/grc

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
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/gnuradio/grc/blocks" TYPE FILE FILES
    "/home/lmz/gr-radar/grc/radar_signal_generator_cw_c.block.yml"
    "/home/lmz/gr-radar/grc/radar_signal_generator_fmcw_c.block.yml"
    "/home/lmz/gr-radar/grc/radar_split_cc.block.yml"
    "/home/lmz/gr-radar/grc/radar_os_cfar_c.block.yml"
    "/home/lmz/gr-radar/grc/radar_ts_fft_cc.block.yml"
    "/home/lmz/gr-radar/grc/radar_estimator_cw.block.yml"
    "/home/lmz/gr-radar/grc/radar_print_results.block.yml"
    "/home/lmz/gr-radar/grc/radar_static_target_simulator_cc.block.yml"
    "/home/lmz/gr-radar/grc/radar_signal_generator_fsk_c.block.yml"
    "/home/lmz/gr-radar/grc/radar_split_fsk_cc.block.yml"
    "/home/lmz/gr-radar/grc/radar_estimator_fsk.block.yml"
    "/home/lmz/gr-radar/grc/radar_usrp_echotimer_cc.block.yml"
    "/home/lmz/gr-radar/grc/radar_estimator_fmcw.block.yml"
    "/home/lmz/gr-radar/grc/radar_signal_generator_sync_pulse_c.block.yml"
    "/home/lmz/gr-radar/grc/radar_estimator_sync_pulse_c.block.yml"
    "/home/lmz/gr-radar/grc/radar_find_max_peak_c.block.yml"
    "/home/lmz/gr-radar/grc/radar_qtgui_scatter_plot.block.yml"
    "/home/lmz/gr-radar/grc/radar_qtgui_time_plot.block.yml"
    "/home/lmz/gr-radar/grc/radar_tracking_singletarget.block.yml"
    "/home/lmz/gr-radar/grc/radar_msg_gate.block.yml"
    "/home/lmz/gr-radar/grc/radar_msg_manipulator.block.yml"
    "/home/lmz/gr-radar/grc/radar_ofdm_cyclic_prefix_remover_cvc.block.yml"
    "/home/lmz/gr-radar/grc/radar_transpose_matrix_vcvc.block.yml"
    "/home/lmz/gr-radar/grc/radar_qtgui_spectrogram_plot.block.yml"
    "/home/lmz/gr-radar/grc/radar_crop_matrix_vcvc.block.yml"
    "/home/lmz/gr-radar/grc/radar_ofdm_divide_vcvc.block.yml"
    "/home/lmz/gr-radar/grc/radar_os_cfar_2d_vc.block.yml"
    "/home/lmz/gr-radar/grc/radar_estimator_ofdm.block.yml"
    "/home/lmz/gr-radar/grc/radar_estimator_rcs.block.yml"
    "/home/lmz/gr-radar/grc/radar_trigger_command.block.yml"
    )
endif()

