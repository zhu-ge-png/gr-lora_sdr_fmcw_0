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


 
 static const char *__doc_gr_radar_signal_generator_sync_pulse_c = R"doc(This block generates a signal for the synchronization of the USRP Echotimer in baseband. The signal is pulsed with a constant amplitude with various pulse length and wait samples in between. It is structured by alternating wait parts and burst parts and starting with the first wait part. The pulses are full real signals.

Constructor Specific Documentation:

Return a shared_ptr to a new instance of radar::signal_generator_sync_pulse_c.

To avoid accidental use of raw pointers, radar::signal_generator_sync_pulse_c's constructor is in a private implementation class. radar::signal_generator_sync_pulse_c::make is the public interface for creating new instances.

Args:
    packet_len : 
    pulse_len : 
    pulse_pause : 
    pulse_amplitude : 
    len_key : )doc";


 static const char *__doc_gr_radar_signal_generator_sync_pulse_c_signal_generator_sync_pulse_c = R"doc()doc";


 static const char *__doc_gr_radar_signal_generator_sync_pulse_c_make = R"doc(This block generates a signal for the synchronization of the USRP Echotimer in baseband. The signal is pulsed with a constant amplitude with various pulse length and wait samples in between. It is structured by alternating wait parts and burst parts and starting with the first wait part. The pulses are full real signals.

Constructor Specific Documentation:

Return a shared_ptr to a new instance of radar::signal_generator_sync_pulse_c.

To avoid accidental use of raw pointers, radar::signal_generator_sync_pulse_c's constructor is in a private implementation class. radar::signal_generator_sync_pulse_c::make is the public interface for creating new instances.

Args:
    packet_len : 
    pulse_len : 
    pulse_pause : 
    pulse_amplitude : 
    len_key : )doc";

  
