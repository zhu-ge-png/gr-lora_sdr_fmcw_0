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


 
 static const char *__doc_gr_radar_os_cfar_2d_vc = R"doc(This block estimates peaks of a given matrix. A matrix can be represented as a combination of vectors and tagged streams. Input has to be a matrix with linear scaled values (NOT logarithmic scaled!). Used algorithm is a 2D OS-CFAR algorithm. The algorithm uses around the cell under test (CUT) on each side samp_compare samples to estimate the noise floor. samp_protect is a protected are around the CUT which is not used for acquiring compare samples. Index 0 of a input vector refers to x axis properties and index 1 refers to y axis properties. The relative threshold is defined by the bin of the vector within the sorted samp_compare samples. A standard value is rel_threshold = 0.78. The value of this bin is multiplied by mult_threshold and compared with the CUT. If the magnitude square of the CUT is greater than the threshold the matrix item is accepted. Used identifiers (symbols) for data are 'axis_x', 'axis_y' and 'power'.

Constructor Specific Documentation:

Return a shared_ptr to a new instance of radar::os_cfar_2d_vc.

To avoid accidental use of raw pointers, radar::os_cfar_2d_vc's constructor is in a private implementation class. radar::os_cfar_2d_vc::make is the public interface for creating new instances.

Args:
    vlen : 
    samp_compare : 
    samp_protect : 
    rel_threshold : 
    mult_threshold : 
    len_key : )doc";


 static const char *__doc_gr_radar_os_cfar_2d_vc_os_cfar_2d_vc_0 = R"doc()doc";


 static const char *__doc_gr_radar_os_cfar_2d_vc_os_cfar_2d_vc_1 = R"doc()doc";


 static const char *__doc_gr_radar_os_cfar_2d_vc_make = R"doc(This block estimates peaks of a given matrix. A matrix can be represented as a combination of vectors and tagged streams. Input has to be a matrix with linear scaled values (NOT logarithmic scaled!). Used algorithm is a 2D OS-CFAR algorithm. The algorithm uses around the cell under test (CUT) on each side samp_compare samples to estimate the noise floor. samp_protect is a protected are around the CUT which is not used for acquiring compare samples. Index 0 of a input vector refers to x axis properties and index 1 refers to y axis properties. The relative threshold is defined by the bin of the vector within the sorted samp_compare samples. A standard value is rel_threshold = 0.78. The value of this bin is multiplied by mult_threshold and compared with the CUT. If the magnitude square of the CUT is greater than the threshold the matrix item is accepted. Used identifiers (symbols) for data are 'axis_x', 'axis_y' and 'power'.

Constructor Specific Documentation:

Return a shared_ptr to a new instance of radar::os_cfar_2d_vc.

To avoid accidental use of raw pointers, radar::os_cfar_2d_vc's constructor is in a private implementation class. radar::os_cfar_2d_vc::make is the public interface for creating new instances.

Args:
    vlen : 
    samp_compare : 
    samp_protect : 
    rel_threshold : 
    mult_threshold : 
    len_key : )doc";


 static const char *__doc_gr_radar_os_cfar_2d_vc_set_rel_threshold = R"doc()doc";


 static const char *__doc_gr_radar_os_cfar_2d_vc_set_mult_threshold = R"doc()doc";


 static const char *__doc_gr_radar_os_cfar_2d_vc_set_samp_compare = R"doc()doc";


 static const char *__doc_gr_radar_os_cfar_2d_vc_set_samp_protect = R"doc()doc";

  
