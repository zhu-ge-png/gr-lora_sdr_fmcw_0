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


 
 static const char *__doc_gr_radar_transpose_matrix_vcvc = R"doc(This block transposes a matrix. A tagged stream combined with vectors as items represent a matrix. vlen_in is the vector length of the input data and vlen_out the vector length of the output data. vlen_out is equal to the items (vectors) per tagged stream on the input stream.

Constructor Specific Documentation:

Return a shared_ptr to a new instance of radar::transpose_matrix_vcvc.

To avoid accidental use of raw pointers, radar::transpose_matrix_vcvc's constructor is in a private implementation class. radar::transpose_matrix_vcvc::make is the public interface for creating new instances.

Args:
    vlen_in : 
    vlen_out : 
    len_key : )doc";


 static const char *__doc_gr_radar_transpose_matrix_vcvc_transpose_matrix_vcvc = R"doc()doc";


 static const char *__doc_gr_radar_transpose_matrix_vcvc_make = R"doc(This block transposes a matrix. A tagged stream combined with vectors as items represent a matrix. vlen_in is the vector length of the input data and vlen_out the vector length of the output data. vlen_out is equal to the items (vectors) per tagged stream on the input stream.

Constructor Specific Documentation:

Return a shared_ptr to a new instance of radar::transpose_matrix_vcvc.

To avoid accidental use of raw pointers, radar::transpose_matrix_vcvc's constructor is in a private implementation class. radar::transpose_matrix_vcvc::make is the public interface for creating new instances.

Args:
    vlen_in : 
    vlen_out : 
    len_key : )doc";

  
