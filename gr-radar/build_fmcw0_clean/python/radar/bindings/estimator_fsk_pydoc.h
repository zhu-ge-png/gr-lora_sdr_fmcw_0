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


 
 static const char *__doc_gr_radar_estimator_fsk = R"doc(This block estimates the range with peaks given from a FSK spectrum. Needed identifiers (symbols) are 'frequency' and 'phase'. The velocity is calculated with the 'frequency' information and the doppler formula. The phase of the doppler peaks are used to estimate the range. Output identifier are 'range' and 'velocity'. If push_power is true the information about the power of the peaks is pushed through. This can be used for estimating the RCS of an object.

Constructor Specific Documentation:

Return a shared_ptr to a new instance of radar::estimator_fsk.

To avoid accidental use of raw pointers, radar::estimator_fsk's constructor is in a private implementation class. radar::estimator_fsk::make is the public interface for creating new instances.

Args:
    center_freq : 
    delta_freq : 
    push_power : )doc";


 static const char *__doc_gr_radar_estimator_fsk_estimator_fsk = R"doc()doc";


 static const char *__doc_gr_radar_estimator_fsk_make = R"doc(This block estimates the range with peaks given from a FSK spectrum. Needed identifiers (symbols) are 'frequency' and 'phase'. The velocity is calculated with the 'frequency' information and the doppler formula. The phase of the doppler peaks are used to estimate the range. Output identifier are 'range' and 'velocity'. If push_power is true the information about the power of the peaks is pushed through. This can be used for estimating the RCS of an object.

Constructor Specific Documentation:

Return a shared_ptr to a new instance of radar::estimator_fsk.

To avoid accidental use of raw pointers, radar::estimator_fsk's constructor is in a private implementation class. radar::estimator_fsk::make is the public interface for creating new instances.

Args:
    center_freq : 
    delta_freq : 
    push_power : )doc";

  
