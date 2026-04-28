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


 
 static const char *__doc_gr_radar_tracking_singletarget = R"doc(This block tracks a singletarget detection with a particle or kalman filter. As input values with identifiers 'range' and 'velocity' are needed and should hold a f32vector with only one element. All input variables tagged with std gives the standard deviation of the parameter. The threshold_track is a value which decides with the likelihood of the data if the new data is accepted as a track. A good starting value is threshold_track = 0.001. threshold_lost is the number of false tracks unitel the track is lost and the tracker begins with a new one. The string filter decides which tracking kernel should be used. 'kalman' or 'particle' are valid. If 'particle' is chosen num_particle gives the number of particles for the particle filter. If 'kalman' is chosen there is no effect on the tracker.

Constructor Specific Documentation:

Return a shared_ptr to a new instance of radar::tracking_singletarget.

To avoid accidental use of raw pointers, radar::tracking_singletarget's constructor is in a private implementation class. radar::tracking_singletarget::make is the public interface for creating new instances.

Args:
    num_particle : 
    std_range_meas : 
    std_velocity_meas : 
    std_accel_sys : 
    threshold_track : 
    threshold_lost : 
    filter : )doc";


 static const char *__doc_gr_radar_tracking_singletarget_tracking_singletarget = R"doc()doc";


 static const char *__doc_gr_radar_tracking_singletarget_make = R"doc(This block tracks a singletarget detection with a particle or kalman filter. As input values with identifiers 'range' and 'velocity' are needed and should hold a f32vector with only one element. All input variables tagged with std gives the standard deviation of the parameter. The threshold_track is a value which decides with the likelihood of the data if the new data is accepted as a track. A good starting value is threshold_track = 0.001. threshold_lost is the number of false tracks unitel the track is lost and the tracker begins with a new one. The string filter decides which tracking kernel should be used. 'kalman' or 'particle' are valid. If 'particle' is chosen num_particle gives the number of particles for the particle filter. If 'kalman' is chosen there is no effect on the tracker.

Constructor Specific Documentation:

Return a shared_ptr to a new instance of radar::tracking_singletarget.

To avoid accidental use of raw pointers, radar::tracking_singletarget's constructor is in a private implementation class. radar::tracking_singletarget::make is the public interface for creating new instances.

Args:
    num_particle : 
    std_range_meas : 
    std_velocity_meas : 
    std_accel_sys : 
    threshold_track : 
    threshold_lost : 
    filter : )doc";

  
