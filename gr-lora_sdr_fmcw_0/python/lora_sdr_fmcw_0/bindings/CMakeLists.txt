# Copyright 2020 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

########################################################################
# Check if there is C++ code at all
########################################################################
if(NOT lora_sdr_fmcw_0_sources)
    MESSAGE(STATUS "No C++ sources... skipping python bindings")
    return()
endif(NOT lora_sdr_fmcw_0_sources)

########################################################################
# Check for pygccxml
########################################################################
GR_PYTHON_CHECK_MODULE_RAW(
    "pygccxml"
    "import pygccxml"
    PYGCCXML_FOUND
    )

include(GrPybind)

########################################################################
# Python Bindings
########################################################################

list(APPEND lora_sdr_fmcw_0_python_files
        add_crc_python.cc
        crc_verif_python.cc
        data_source_python.cc
        deinterleaver_python.cc
        dewhitening_python.cc
        fft_demod_python.cc
        frame_sync_python.cc
        frame_sync0_python.cc
        gray_demap_python.cc
        gray_mapping_python.cc
        hamming_dec_python.cc
        hamming_enc_python.cc
        header_decoder_python.cc
        header_python.cc
        interleaver_python.cc
        modulate_python.cc
        modulate0_python.cc
        radar_estimator_updown0_python.cc
        radar_rx0_python.cc
        payload_id_inc_python.cc
        RH_RF95_header_python.cc
        whitening_python.cc
        python_bindings.cc)

GR_PYBIND_MAKE_OOT(lora_sdr_fmcw_0
   ../../..
   gr::lora_sdr_fmcw_0
   "${lora_sdr_fmcw_0_python_files}")

# copy bindings extension for use in QA test module
add_custom_command(TARGET lora_sdr_fmcw_0_python POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:lora_sdr_fmcw_0_python>
    ${CMAKE_BINARY_DIR}/test_modules/gnuradio/lora_sdr_fmcw_0/
)

install(TARGETS lora_sdr_fmcw_0_python DESTINATION ${GR_PYTHON_DIR}/gnuradio/lora_sdr_fmcw_0 COMPONENT pythonapi)
