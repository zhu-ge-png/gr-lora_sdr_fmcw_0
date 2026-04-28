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


 
 static const char *__doc_gr_radar_estimator_cw = R"doc(This block estimates the velocity from given peaks of a CW spectrum. The estimator looks for a f32vector tagged with a 'frequency' identifier (symbol) and calculates the velocity with the doppler formula. The identifier (symbol) of the output data is 'velocity'. Needed identifier (symbols) of the input are 'frequency'.

Constructor Specific Documentation:

Return a shared_ptr to a new instance of radar::estimator_cw.

To avoid accidental use of raw pointers, radar::estimator_cw's constructor is in a private implementation class. radar::estimator_cw::make is the public interface for creating new instances.

Args:
    center_freq : )doc";


 static const char *__doc_gr_radar_estimator_cw_estimator_cw = R"doc()doc";


 static const char *__doc_gr_radar_estimator_cw_make = R"doc(This block estimates the velocity from given peaks of a CW spectrum. The estimator looks for a f32vector tagged with a 'frequency' identifier (symbol) and calculates the velocity with the doppler formula. The identifier (symbol) of the output data is 'velocity'. Needed identifier (symbols) of the input are 'frequency'.

Constructor Specific Documentation:

Return a shared_ptr to a new instance of radar::estimator_cw.

To avoid accidental use of raw pointers, radar::estimator_cw's constructor is in a private implementation class. radar::estimator_cw::make is the public interface for creating new instances.

Args:
    center_freq : )doc";

  
