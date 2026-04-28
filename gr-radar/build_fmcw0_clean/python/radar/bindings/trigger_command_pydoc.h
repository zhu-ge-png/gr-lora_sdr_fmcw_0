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


 
 static const char *__doc_gr_radar_trigger_command = R"doc(This block executes a command with the std::system() command if a value from a f32vector with a given identifier (symbol) is in a given range. Each index of a vector refers to a identifier. The execution of a command can be blocked for block_time milliseconds after the last execution.

Constructor Specific Documentation:

Return a shared_ptr to a new instance of radar::trigger_command.

To avoid accidental use of raw pointers, radar::trigger_command's constructor is in a private implementation class. radar::trigger_command::make is the public interface for creating new instances.

Args:
    command : 
    identifiers : 
    vals_min : 
    vals_max : 
    block_time : )doc";


 static const char *__doc_gr_radar_trigger_command_trigger_command = R"doc()doc";


 static const char *__doc_gr_radar_trigger_command_make = R"doc(This block executes a command with the std::system() command if a value from a f32vector with a given identifier (symbol) is in a given range. Each index of a vector refers to a identifier. The execution of a command can be blocked for block_time milliseconds after the last execution.

Constructor Specific Documentation:

Return a shared_ptr to a new instance of radar::trigger_command.

To avoid accidental use of raw pointers, radar::trigger_command's constructor is in a private implementation class. radar::trigger_command::make is the public interface for creating new instances.

Args:
    command : 
    identifiers : 
    vals_min : 
    vals_max : 
    block_time : )doc";

  
