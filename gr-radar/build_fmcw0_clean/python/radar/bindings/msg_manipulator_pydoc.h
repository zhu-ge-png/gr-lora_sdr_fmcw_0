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


 
 static const char *__doc_gr_radar_msg_manipulator = R"doc(This block manipulates data in a msg with given identifier (symbol). All data are given as vectors and each index represents a dataset with identifier which should be processed. All other data is pushed through. The addition is performed before the multiplication.

Constructor Specific Documentation:

Return a shared_ptr to a new instance of radar::msg_manipulator.

To avoid accidental use of raw pointers, radar::msg_manipulator's constructor is in a private implementation class. radar::msg_manipulator::make is the public interface for creating new instances.

Args:
    symbols : 
    const_add : 
    const_mult : )doc";


 static const char *__doc_gr_radar_msg_manipulator_msg_manipulator_0 = R"doc()doc";


 static const char *__doc_gr_radar_msg_manipulator_msg_manipulator_1 = R"doc()doc";


 static const char *__doc_gr_radar_msg_manipulator_make = R"doc(This block manipulates data in a msg with given identifier (symbol). All data are given as vectors and each index represents a dataset with identifier which should be processed. All other data is pushed through. The addition is performed before the multiplication.

Constructor Specific Documentation:

Return a shared_ptr to a new instance of radar::msg_manipulator.

To avoid accidental use of raw pointers, radar::msg_manipulator's constructor is in a private implementation class. radar::msg_manipulator::make is the public interface for creating new instances.

Args:
    symbols : 
    const_add : 
    const_mult : )doc";


 static const char *__doc_gr_radar_msg_manipulator_set_const_add = R"doc()doc";


 static const char *__doc_gr_radar_msg_manipulator_set_const_mult = R"doc()doc";

  
