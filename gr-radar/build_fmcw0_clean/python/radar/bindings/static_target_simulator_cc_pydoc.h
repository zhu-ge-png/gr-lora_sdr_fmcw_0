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


 
 static const char *__doc_gr_radar_static_target_simulator_cc = R"doc(Simulates the backscattering of a given signal on point targets.


Implements the point scatter model. The input signal is the transmitted signal. The output signal is the received, backscattered signal, and contains one output signal per receive antenna.



Target modeling
The targets are modeled by the vectors , , , and . All these vectors need to be of length H, where H describes the number of reflecting targets. The backscattered signal can either have a zero phase, or a random phase (controlled by ). The received signal will be the linear superposition of H signals, each of which are derived from the input signal by the following equation:





The attenuation depends on the center frequency , the radar cross section , the distance of the target  and the speed of light :  


The delay  depends on the distance of the target:  


The Doppler shift  depends on the relative velocity and the center frequency:  


The signals are added up to produce the total sum signal:  




MIMO processing simulation
This block has a limited capability of simulating multi-antenna reception. The  vector determines the distance of every RX antenna from the origin (Note: The TX antenna is always in the origin). The length of the  vector is thus also the number of output signals this block produces. For a simple, mono-static SISO radar, simply set position_rx to [0]. The RX antennas are always laid out in a straight line. When multiple antennas are given, the target azimuth plays a role; an azimuth of zero is perpendicular to the line in which the RX antennas are placed.




Self-coupling
Self-coupling describes the amount of the TX signal that is directly coupled into the RX path. When  is set to true, effectively, a target with zero velocity and range is added. The parameter  describes the attenuation of the self-coupling, a value of -10 means that the transmit signal is attenuated by 10 dB on the receive signal.

Constructor Specific Documentation:



Args:
    range : Target ranges as vector (length H)
    velocity : Target velocities as vector (length H)
    rcs : Target RCS as vector (length H)
    azimuth : Target azimuth as vector (length H)
    position_rx : Position RX antennas. A value of [0] means there is one antenna, located in the origin (simple monostatic case).
    samp_rate : Sample rate (samples per second)
    center_freq : Center frequency (Hz)
    self_coupling_db : Self coupling attenuation (dB)
    rndm_phaseshift : Toggle random phaseshift on targets
    self_coupling : Toggle self coupling
    packet_len : Packet length key for tagged stream)doc";


 static const char *__doc_gr_radar_static_target_simulator_cc_static_target_simulator_cc_0 = R"doc()doc";


 static const char *__doc_gr_radar_static_target_simulator_cc_static_target_simulator_cc_1 = R"doc()doc";


 static const char *__doc_gr_radar_static_target_simulator_cc_make = R"doc(Simulates the backscattering of a given signal on point targets.


Implements the point scatter model. The input signal is the transmitted signal. The output signal is the received, backscattered signal, and contains one output signal per receive antenna.



Target modeling
The targets are modeled by the vectors , , , and . All these vectors need to be of length H, where H describes the number of reflecting targets. The backscattered signal can either have a zero phase, or a random phase (controlled by ). The received signal will be the linear superposition of H signals, each of which are derived from the input signal by the following equation:





The attenuation depends on the center frequency , the radar cross section , the distance of the target  and the speed of light :  


The delay  depends on the distance of the target:  


The Doppler shift  depends on the relative velocity and the center frequency:  


The signals are added up to produce the total sum signal:  




MIMO processing simulation
This block has a limited capability of simulating multi-antenna reception. The  vector determines the distance of every RX antenna from the origin (Note: The TX antenna is always in the origin). The length of the  vector is thus also the number of output signals this block produces. For a simple, mono-static SISO radar, simply set position_rx to [0]. The RX antennas are always laid out in a straight line. When multiple antennas are given, the target azimuth plays a role; an azimuth of zero is perpendicular to the line in which the RX antennas are placed.




Self-coupling
Self-coupling describes the amount of the TX signal that is directly coupled into the RX path. When  is set to true, effectively, a target with zero velocity and range is added. The parameter  describes the attenuation of the self-coupling, a value of -10 means that the transmit signal is attenuated by 10 dB on the receive signal.

Constructor Specific Documentation:



Args:
    range : Target ranges as vector (length H)
    velocity : Target velocities as vector (length H)
    rcs : Target RCS as vector (length H)
    azimuth : Target azimuth as vector (length H)
    position_rx : Position RX antennas. A value of [0] means there is one antenna, located in the origin (simple monostatic case).
    samp_rate : Sample rate (samples per second)
    center_freq : Center frequency (Hz)
    self_coupling_db : Self coupling attenuation (dB)
    rndm_phaseshift : Toggle random phaseshift on targets
    self_coupling : Toggle self coupling
    packet_len : Packet length key for tagged stream)doc";


 static const char *__doc_gr_radar_static_target_simulator_cc_setup_targets = R"doc()doc";

  
