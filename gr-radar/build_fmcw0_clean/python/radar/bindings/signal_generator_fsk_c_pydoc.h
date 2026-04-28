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


 
 static const char *__doc_gr_radar_signal_generator_fsk_c = R"doc(This block generates a signal for FSK radar in baseband. The waveform consists of a signal with an alternating frequency. The packet length for subsequent tagged streams is calculated with two times the samples per single frequency multiplied by the blocks per tag.

Constructor Specific Documentation:

Return a shared_ptr to a new instance of radar::signal_generator_fsk_c.

To avoid accidental use of raw pointers, radar::signal_generator_fsk_c's constructor is in a private implementation class. radar::signal_generator_fsk_c::make is the public interface for creating new instances.

Args:
    samp_rate : 
    samp_per_freq : 
    blocks_per_tag : 
    freq_low : 
    freq_high : 
    amplitude : 
    len_key : )doc";


 static const char *__doc_gr_radar_signal_generator_fsk_c_signal_generator_fsk_c = R"doc()doc";


 static const char *__doc_gr_radar_signal_generator_fsk_c_make = R"doc(This block generates a signal for FSK radar in baseband. The waveform consists of a signal with an alternating frequency. The packet length for subsequent tagged streams is calculated with two times the samples per single frequency multiplied by the blocks per tag.

Constructor Specific Documentation:

Return a shared_ptr to a new instance of radar::signal_generator_fsk_c.

To avoid accidental use of raw pointers, radar::signal_generator_fsk_c's constructor is in a private implementation class. radar::signal_generator_fsk_c::make is the public interface for creating new instances.

Args:
    samp_rate : 
    samp_per_freq : 
    blocks_per_tag : 
    freq_low : 
    freq_high : 
    amplitude : 
    len_key : )doc";

  
