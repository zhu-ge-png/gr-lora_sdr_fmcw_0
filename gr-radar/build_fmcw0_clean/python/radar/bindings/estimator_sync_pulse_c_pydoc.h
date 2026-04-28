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


 
 static const char *__doc_gr_radar_estimator_sync_pulse_c = R"doc(This block can be used to estimate the shift of a signal on input 1 in relation to another on input 2. For example the constant number of delay samples due to hardware effect from a signal source can be estimated. The calculation of the shift is done by a cross correlation of the input signals. The number of correlations in samples is given with num_xcorr. The output message is the number of delay samples with the identifier (symbol) 'sync_pulse'. This can be displayed with the 'Print Results' block.

Constructor Specific Documentation:

Return a shared_ptr to a new instance of radar::estimator_sync_pulse_c.

To avoid accidental use of raw pointers, radar::estimator_sync_pulse_c's constructor is in a private implementation class. radar::estimator_sync_pulse_c::make is the public interface for creating new instances.

Args:
    num_xcorr : 
    len_key : )doc";


 static const char *__doc_gr_radar_estimator_sync_pulse_c_estimator_sync_pulse_c_0 = R"doc()doc";


 static const char *__doc_gr_radar_estimator_sync_pulse_c_estimator_sync_pulse_c_1 = R"doc()doc";


 static const char *__doc_gr_radar_estimator_sync_pulse_c_make = R"doc(This block can be used to estimate the shift of a signal on input 1 in relation to another on input 2. For example the constant number of delay samples due to hardware effect from a signal source can be estimated. The calculation of the shift is done by a cross correlation of the input signals. The number of correlations in samples is given with num_xcorr. The output message is the number of delay samples with the identifier (symbol) 'sync_pulse'. This can be displayed with the 'Print Results' block.

Constructor Specific Documentation:

Return a shared_ptr to a new instance of radar::estimator_sync_pulse_c.

To avoid accidental use of raw pointers, radar::estimator_sync_pulse_c's constructor is in a private implementation class. radar::estimator_sync_pulse_c::make is the public interface for creating new instances.

Args:
    num_xcorr : 
    len_key : )doc";


 static const char *__doc_gr_radar_estimator_sync_pulse_c_set_num_xcorr = R"doc()doc";

  
