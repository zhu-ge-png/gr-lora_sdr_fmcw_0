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


 
 static const char *__doc_gr_radar_msg_gate = R"doc(This block blocks messages whose data is not in range of val_min to val_max. All parameters are given as vectors. Each index represents a dataset with given identifier (symbol) which should be tested on valid data in given range. All other data is pushed through.

Constructor Specific Documentation:

Return a shared_ptr to a new instance of radar::msg_gate.

To avoid accidental use of raw pointers, radar::msg_gate's constructor is in a private implementation class. radar::msg_gate::make is the public interface for creating new instances.

Args:
    keys : 
    val_min : 
    val_max : )doc";


 static const char *__doc_gr_radar_msg_gate_msg_gate = R"doc()doc";


 static const char *__doc_gr_radar_msg_gate_make = R"doc(This block blocks messages whose data is not in range of val_min to val_max. All parameters are given as vectors. Each index represents a dataset with given identifier (symbol) which should be tested on valid data in given range. All other data is pushed through.

Constructor Specific Documentation:

Return a shared_ptr to a new instance of radar::msg_gate.

To avoid accidental use of raw pointers, radar::msg_gate's constructor is in a private implementation class. radar::msg_gate::make is the public interface for creating new instances.

Args:
    keys : 
    val_min : 
    val_max : )doc";

  
