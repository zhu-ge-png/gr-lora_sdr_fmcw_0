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


 
 static const char *__doc_gr_radar_estimator_rcs = R"doc(Basic RCS block for estimating the RCS of a single target. Some hardware specs need to be known for calculating RCS values, see parameters for details. The radar equation is used to calculate the RCS: RCS = Pr*(4pi)^3*R^4/(Pt*Gt*Gr*lamda^2). The Rx power (Pr) and the distance (R) are being estimated, while the other parameters are given in the flowgraph. It is possible to average a number of samples by setting the num_mean value > 1. The RCS will be 0 until enough samples are collected to calculate the mean value (be patient). The Tx power (Pt) needs to be calibrated with external hardware. I recommend to calibrate for the wanted power and not to change the parameters in the flowgraph on the Tx side after that. The RCS block needs the Rx power, to estimate the RCS. For that, the input power of the block needs to be determined analytically and altered via the corr_factor and exponent values, to fit the following equation: Pr = P_input ^ (exponent) * corr_factor / Pt. In addition, the FFTs need to be normalized for correct power calculation.

Constructor Specific Documentation:

Return a shared_ptr to a new instance of radar::estimator_rcs.

To avoid accidental use of raw pointers, radar::estimator_rcs's constructor is in a private implementation class. radar::estimator_rcs::make is the public interface for creating new instances.

Args:
    num_mean : 
    center_freq : 
    antenna_gain_tx : 
    antenna_gain_rx : 
    usrp_gain_rx : 
    power_tx : 
    corr_factor : 
    exponent : )doc";


 static const char *__doc_gr_radar_estimator_rcs_estimator_rcs_0 = R"doc()doc";


 static const char *__doc_gr_radar_estimator_rcs_estimator_rcs_1 = R"doc()doc";


 static const char *__doc_gr_radar_estimator_rcs_make = R"doc(Basic RCS block for estimating the RCS of a single target. Some hardware specs need to be known for calculating RCS values, see parameters for details. The radar equation is used to calculate the RCS: RCS = Pr*(4pi)^3*R^4/(Pt*Gt*Gr*lamda^2). The Rx power (Pr) and the distance (R) are being estimated, while the other parameters are given in the flowgraph. It is possible to average a number of samples by setting the num_mean value > 1. The RCS will be 0 until enough samples are collected to calculate the mean value (be patient). The Tx power (Pt) needs to be calibrated with external hardware. I recommend to calibrate for the wanted power and not to change the parameters in the flowgraph on the Tx side after that. The RCS block needs the Rx power, to estimate the RCS. For that, the input power of the block needs to be determined analytically and altered via the corr_factor and exponent values, to fit the following equation: Pr = P_input ^ (exponent) * corr_factor / Pt. In addition, the FFTs need to be normalized for correct power calculation.

Constructor Specific Documentation:

Return a shared_ptr to a new instance of radar::estimator_rcs.

To avoid accidental use of raw pointers, radar::estimator_rcs's constructor is in a private implementation class. radar::estimator_rcs::make is the public interface for creating new instances.

Args:
    num_mean : 
    center_freq : 
    antenna_gain_tx : 
    antenna_gain_rx : 
    usrp_gain_rx : 
    power_tx : 
    corr_factor : 
    exponent : )doc";


 static const char *__doc_gr_radar_estimator_rcs_set_num_mean = R"doc()doc";


 static const char *__doc_gr_radar_estimator_rcs_set_center_freq = R"doc()doc";


 static const char *__doc_gr_radar_estimator_rcs_set_antenna_gain_tx = R"doc()doc";


 static const char *__doc_gr_radar_estimator_rcs_set_antenna_gain_rx = R"doc()doc";


 static const char *__doc_gr_radar_estimator_rcs_set_usrp_gain_rx = R"doc()doc";


 static const char *__doc_gr_radar_estimator_rcs_set_power_tx = R"doc()doc";


 static const char *__doc_gr_radar_estimator_rcs_set_corr_factor = R"doc()doc";

  
