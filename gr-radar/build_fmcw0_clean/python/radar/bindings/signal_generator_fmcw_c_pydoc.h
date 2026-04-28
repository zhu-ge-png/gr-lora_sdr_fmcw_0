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


 
 static const char *__doc_gr_radar_signal_generator_fmcw_c = R"doc(Generates a signal for FMCW radar in baseband.


The generated signal consists of three parts, in this order:






The up-chirp goes from CW frequency to CW frequency plus sweep frequency and the down-chirp goes in the opposite direction. All of these parts can be disabled by setting the corresponding length to zero.


The packet length for subsequent tagged streams is calculated by the sum of the number of samples of the single modulations parts.

Constructor Specific Documentation:



Args:
    samp_rate : Signal sample rate (samples per second)
    samp_up : Number samples of up-chirp part
    samp_down : Number samples of down-chirp part
    samp_cw : Number samples of CW part
    freq_cw : CW signal frequency in baseband
    freq_sweep : Sweep frequency of up- and down-chirp
    amplitude : Signal amplitude
    len_key : Packet length key for tagged stream)doc";


 static const char *__doc_gr_radar_signal_generator_fmcw_c_signal_generator_fmcw_c = R"doc()doc";


 static const char *__doc_gr_radar_signal_generator_fmcw_c_make = R"doc(Generates a signal for FMCW radar in baseband.


The generated signal consists of three parts, in this order:






The up-chirp goes from CW frequency to CW frequency plus sweep frequency and the down-chirp goes in the opposite direction. All of these parts can be disabled by setting the corresponding length to zero.


The packet length for subsequent tagged streams is calculated by the sum of the number of samples of the single modulations parts.

Constructor Specific Documentation:



Args:
    samp_rate : Signal sample rate (samples per second)
    samp_up : Number samples of up-chirp part
    samp_down : Number samples of down-chirp part
    samp_cw : Number samples of CW part
    freq_cw : CW signal frequency in baseband
    freq_sweep : Sweep frequency of up- and down-chirp
    amplitude : Signal amplitude
    len_key : Packet length key for tagged stream)doc";

  
