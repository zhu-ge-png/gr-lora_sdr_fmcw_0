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


 
 static const char *__doc_gr_radar_estimator_ofdm = R"doc(This block evaluates the peaks given from a OFDM matrix. Input are the bins of the peaks with the identifiers 'axis_x' and 'axis_y'. The parameters of the block axis_x and axis_y are vectors which define the mapping of the axis. If two values are given it is assumed a linear progression in between. If four values are given the middle values are set on half of the axis and it is interpolated linear in between. len_x and len_y gives the length of the axis in number of bins. symbol_x and symbol_y defines the identifier (symbols) for the output data. merge_consecutive toggles merging consecutive peaks. Each peak is compared with peaks in a range of one bin. If there is a peak with a higher power the actual bin is not used for evaluations. If merge_consecutive is true data with identifier 'power' is needed.

Constructor Specific Documentation:

Return a shared_ptr to a new instance of radar::estimator_ofdm.

To avoid accidental use of raw pointers, radar::estimator_ofdm's constructor is in a private implementation class. radar::estimator_ofdm::make is the public interface for creating new instances.

Args:
    symbol_x : 
    len_x : 
    axis_x : 
    symbol_y : 
    len_y : 
    axis_y : 
    merge_consecutive : )doc";


 static const char *__doc_gr_radar_estimator_ofdm_estimator_ofdm = R"doc()doc";


 static const char *__doc_gr_radar_estimator_ofdm_make = R"doc(This block evaluates the peaks given from a OFDM matrix. Input are the bins of the peaks with the identifiers 'axis_x' and 'axis_y'. The parameters of the block axis_x and axis_y are vectors which define the mapping of the axis. If two values are given it is assumed a linear progression in between. If four values are given the middle values are set on half of the axis and it is interpolated linear in between. len_x and len_y gives the length of the axis in number of bins. symbol_x and symbol_y defines the identifier (symbols) for the output data. merge_consecutive toggles merging consecutive peaks. Each peak is compared with peaks in a range of one bin. If there is a peak with a higher power the actual bin is not used for evaluations. If merge_consecutive is true data with identifier 'power' is needed.

Constructor Specific Documentation:

Return a shared_ptr to a new instance of radar::estimator_ofdm.

To avoid accidental use of raw pointers, radar::estimator_ofdm's constructor is in a private implementation class. radar::estimator_ofdm::make is the public interface for creating new instances.

Args:
    symbol_x : 
    len_x : 
    axis_x : 
    symbol_y : 
    len_y : 
    axis_y : 
    merge_consecutive : )doc";

  
