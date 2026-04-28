/*
 * Copyright 2022 Free Software Foundation, Inc.
 *
 * This file is part of GNU Radio
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */
#include "pydoc_macros.h"
#define D(...) DOC(gr,radar, __VA_ARGS__ )
/*
  This file contains placeholders for docstrings for the Python bindings.
  Do not edit! These were automatically extracted during the binding process
  and will be overwritten during the build process
 */


 
 static const char *__doc_gr_radar_split_fsk_cc = R"doc(This block splits a FSK signal consisting of two separate signals. samp_per_freq items are taken and pushed alternating to the outputs. Discarded samples are thrown away at the beginning of samp_per_freq samples and only samp_per_freq-samp_discard are pushed to output.

Constructor Specific Documentation:

Return a shared_ptr to a new instance of radar::split_fsk_cc.

To avoid accidental use of raw pointers, radar::split_fsk_cc's constructor is in a private implementation class. radar::split_fsk_cc::make is the public interface for creating new instances.

Args:
    samp_per_freq : 
    samp_discard : 
    len_key : )doc";


 static const char *__doc_gr_radar_split_fsk_cc_split_fsk_cc = R"doc()doc";


 static const char *__doc_gr_radar_split_fsk_cc_make = R"doc(This block splits a FSK signal consisting of two separate signals. samp_per_freq items are taken and pushed alternating to the outputs. Discarded samples are thrown away at the beginning of samp_per_freq samples and only samp_per_freq-samp_discard are pushed to output.

Constructor Specific Documentation:

Return a shared_ptr to a new instance of radar::split_fsk_cc.

To avoid accidental use of raw pointers, radar::split_fsk_cc's constructor is in a private implementation class. radar::split_fsk_cc::make is the public interface for creating new instances.

Args:
    samp_per_freq : 
    samp_discard : 
    len_key : )doc";

  
