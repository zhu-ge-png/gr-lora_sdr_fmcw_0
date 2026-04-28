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


 
 static const char *__doc_gr_radar_find_max_peak_c = R"doc(This block estimates a single peak of a given FFT spectrum as tagged stream. Output is a message with the information of frequency, phase and power of the peak as a f32vector with a single item. All data is tagged with the identifiers (symbols) 'frequency', 'phase' and 'power'. The peak is estimated on the whole spectrum or on the range max_freq if cut_max_freq is true. Furthermore a threshold of the spectrum amplitude can be given with threshold. The DC peak can be cut out with the protected samples samp_protect. This value do not evaluate samp_protect samples around the DC peak. If no suitable peak is found the block returns empty vectors with the identifiers.

Constructor Specific Documentation:

Return a shared_ptr to a new instance of radar::find_max_peak_c.

To avoid accidental use of raw pointers, radar::find_max_peak_c's constructor is in a private implementation class. radar::find_max_peak_c::make is the public interface for creating new instances.

Args:
    samp_rate : 
    threshold : 
    samp_protect : 
    max_freq : 
    cut_max_freq : 
    len_key : )doc";


 static const char *__doc_gr_radar_find_max_peak_c_find_max_peak_c_0 = R"doc()doc";


 static const char *__doc_gr_radar_find_max_peak_c_find_max_peak_c_1 = R"doc()doc";


 static const char *__doc_gr_radar_find_max_peak_c_make = R"doc(This block estimates a single peak of a given FFT spectrum as tagged stream. Output is a message with the information of frequency, phase and power of the peak as a f32vector with a single item. All data is tagged with the identifiers (symbols) 'frequency', 'phase' and 'power'. The peak is estimated on the whole spectrum or on the range max_freq if cut_max_freq is true. Furthermore a threshold of the spectrum amplitude can be given with threshold. The DC peak can be cut out with the protected samples samp_protect. This value do not evaluate samp_protect samples around the DC peak. If no suitable peak is found the block returns empty vectors with the identifiers.

Constructor Specific Documentation:

Return a shared_ptr to a new instance of radar::find_max_peak_c.

To avoid accidental use of raw pointers, radar::find_max_peak_c's constructor is in a private implementation class. radar::find_max_peak_c::make is the public interface for creating new instances.

Args:
    samp_rate : 
    threshold : 
    samp_protect : 
    max_freq : 
    cut_max_freq : 
    len_key : )doc";


 static const char *__doc_gr_radar_find_max_peak_c_set_threshold = R"doc()doc";


 static const char *__doc_gr_radar_find_max_peak_c_set_samp_protect = R"doc()doc";


 static const char *__doc_gr_radar_find_max_peak_c_set_max_freq = R"doc()doc";

  
