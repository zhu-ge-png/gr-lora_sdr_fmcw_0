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


 
 static const char *__doc_gr_radar_ofdm_divide_vcvc = R"doc(This block performs a complex complex division with in0/in1. If vlen_out > vlen_in the additional space is filled with zeros. This can be used for zeropadding. discarded_carriers is a vector of the carriers which should be not used and set zero as division result. num_sync_words gives the number of sync words on which the discarded_carriers rule is not applied.

Constructor Specific Documentation:

Return a shared_ptr to a new instance of radar::ofdm_divide_vcvc.

To avoid accidental use of raw pointers, radar::ofdm_divide_vcvc's constructor is in a private implementation class. radar::ofdm_divide_vcvc::make is the public interface for creating new instances.

Args:
    vlen_in : 
    vlen_out : 
    discarded_carriers : 
    num_sync_words : 
    len_key : )doc";


 static const char *__doc_gr_radar_ofdm_divide_vcvc_ofdm_divide_vcvc = R"doc()doc";


 static const char *__doc_gr_radar_ofdm_divide_vcvc_make = R"doc(This block performs a complex complex division with in0/in1. If vlen_out > vlen_in the additional space is filled with zeros. This can be used for zeropadding. discarded_carriers is a vector of the carriers which should be not used and set zero as division result. num_sync_words gives the number of sync words on which the discarded_carriers rule is not applied.

Constructor Specific Documentation:

Return a shared_ptr to a new instance of radar::ofdm_divide_vcvc.

To avoid accidental use of raw pointers, radar::ofdm_divide_vcvc's constructor is in a private implementation class. radar::ofdm_divide_vcvc::make is the public interface for creating new instances.

Args:
    vlen_in : 
    vlen_out : 
    discarded_carriers : 
    num_sync_words : 
    len_key : )doc";

  
