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


 
 static const char *__doc_gr_radar_estimator_fmcw = R"doc(This block estimates range and veloicty from peaks of a FMCW spectrum. Input messages are data with the identifier 'frequency' of the up-chirp, down-chirp and CW part. If data is available on all three message ports the estimation starts. The velocity is estimated with the frequency information of the CW block and the range is estimated with the up and down chirp. If multiple frequencies are given, the velocity is estimated first and associated with the most likely range from the up- and down-chirp. The output identifiers are 'range' and 'velocity'.

Constructor Specific Documentation:

Return a shared_ptr to a new instance of radar::estimator_fmcw.

To avoid accidental use of raw pointers, radar::estimator_fmcw's constructor is in a private implementation class. radar::estimator_fmcw::make is the public interface for creating new instances.

Args:
    samp_rate : 
    center_freq : 
    sweep_freq : 
    samp_up : 
    samp_down : 
    push_power : )doc";


 static const char *__doc_gr_radar_estimator_fmcw_estimator_fmcw = R"doc()doc";


 static const char *__doc_gr_radar_estimator_fmcw_make = R"doc(This block estimates range and veloicty from peaks of a FMCW spectrum. Input messages are data with the identifier 'frequency' of the up-chirp, down-chirp and CW part. If data is available on all three message ports the estimation starts. The velocity is estimated with the frequency information of the CW block and the range is estimated with the up and down chirp. If multiple frequencies are given, the velocity is estimated first and associated with the most likely range from the up- and down-chirp. The output identifiers are 'range' and 'velocity'.

Constructor Specific Documentation:

Return a shared_ptr to a new instance of radar::estimator_fmcw.

To avoid accidental use of raw pointers, radar::estimator_fmcw's constructor is in a private implementation class. radar::estimator_fmcw::make is the public interface for creating new instances.

Args:
    samp_rate : 
    center_freq : 
    sweep_freq : 
    samp_up : 
    samp_down : 
    push_power : )doc";

  
