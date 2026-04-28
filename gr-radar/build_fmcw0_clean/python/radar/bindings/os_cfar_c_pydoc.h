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


 
 static const char *__doc_gr_radar_os_cfar_c = R"doc(This block estimates peaks of a given FFT spectrum as tagged stream. Multi peak detection is implemented with the OS-CFAR algorithm. The algorithm uses around the cell under test (CUT) on each side samp_compare samples to estimate the noise floor. This relative threshold is defined by the bin of the vector within the sorted samp_compare samples. A standard value is rel_threshold = 0.78. The value of this bin is multiplied by mult_threshold and compared with the CUT. samp_protect samples are a protected are which is not used for acquiring compare samples. If consecutive bins are detected as valid peaks it is possible to merge these detections with merge_consecutive = true. Output data are f32vectors with the information of frequency, power and phase. The identifiers (symbols) are 'frequency', 'power' and 'phase'.

Constructor Specific Documentation:

Return a shared_ptr to a new instance of radar::os_cfar_c.

To avoid accidental use of raw pointers, radar::os_cfar_c's constructor is in a private implementation class. radar::os_cfar_c::make is the public interface for creating new instances.

Args:
    samp_rate : 
    samp_compare : 
    samp_protect : 
    rel_threshold : 
    mult_threshold : 
    merge_consecutive : 
    len_key : )doc";


 static const char *__doc_gr_radar_os_cfar_c_os_cfar_c_0 = R"doc()doc";


 static const char *__doc_gr_radar_os_cfar_c_os_cfar_c_1 = R"doc()doc";


 static const char *__doc_gr_radar_os_cfar_c_make = R"doc(This block estimates peaks of a given FFT spectrum as tagged stream. Multi peak detection is implemented with the OS-CFAR algorithm. The algorithm uses around the cell under test (CUT) on each side samp_compare samples to estimate the noise floor. This relative threshold is defined by the bin of the vector within the sorted samp_compare samples. A standard value is rel_threshold = 0.78. The value of this bin is multiplied by mult_threshold and compared with the CUT. samp_protect samples are a protected are which is not used for acquiring compare samples. If consecutive bins are detected as valid peaks it is possible to merge these detections with merge_consecutive = true. Output data are f32vectors with the information of frequency, power and phase. The identifiers (symbols) are 'frequency', 'power' and 'phase'.

Constructor Specific Documentation:

Return a shared_ptr to a new instance of radar::os_cfar_c.

To avoid accidental use of raw pointers, radar::os_cfar_c's constructor is in a private implementation class. radar::os_cfar_c::make is the public interface for creating new instances.

Args:
    samp_rate : 
    samp_compare : 
    samp_protect : 
    rel_threshold : 
    mult_threshold : 
    merge_consecutive : 
    len_key : )doc";


 static const char *__doc_gr_radar_os_cfar_c_set_rel_threshold = R"doc()doc";


 static const char *__doc_gr_radar_os_cfar_c_set_mult_threshold = R"doc()doc";


 static const char *__doc_gr_radar_os_cfar_c_set_samp_compare = R"doc()doc";


 static const char *__doc_gr_radar_os_cfar_c_set_samp_protect = R"doc()doc";

  
