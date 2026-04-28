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


 
 static const char *__doc_gr_radar_print_results = R"doc(This block prints data of messages filled with data of the structure [ [[symbol_0],[data_0]], [[symbol_1],[data_1]], ...] on the command line. Only data of the datatypes f32vector and long, and rx_time tuples are displayed. The output can also be stored in a text file.

Constructor Specific Documentation:

Return a shared_ptr to a new instance of radar::print_results.

To avoid accidental use of raw pointers, radar::print_results's constructor is in a private implementation class. radar::print_results::make is the public interface for creating new instances.

Args:
    store_msg : 
    filename : )doc";


 static const char *__doc_gr_radar_print_results_print_results = R"doc()doc";


 static const char *__doc_gr_radar_print_results_make = R"doc(This block prints data of messages filled with data of the structure [ [[symbol_0],[data_0]], [[symbol_1],[data_1]], ...] on the command line. Only data of the datatypes f32vector and long, and rx_time tuples are displayed. The output can also be stored in a text file.

Constructor Specific Documentation:

Return a shared_ptr to a new instance of radar::print_results.

To avoid accidental use of raw pointers, radar::print_results's constructor is in a private implementation class. radar::print_results::make is the public interface for creating new instances.

Args:
    store_msg : 
    filename : )doc";

  
