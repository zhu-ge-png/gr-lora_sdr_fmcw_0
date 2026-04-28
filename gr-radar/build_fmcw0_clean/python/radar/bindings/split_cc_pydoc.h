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


 
 static const char *__doc_gr_radar_split_cc = R"doc(This block splits a tagged stream into segments. As packet_parts you give the structure of the packet, e.g. (10, 20, 5). With the packet number you can choose which packet shall be pushed to output. Counting begins on zero. E.g. packet_num=1 returns 20 items.

Constructor Specific Documentation:

Return a shared_ptr to a new instance of radar::split_cc.

To avoid accidental use of raw pointers, radar::split_cc's constructor is in a private implementation class. radar::split_cc::make is the public interface for creating new instances.

Args:
    packet_num : 
    packet_parts : 
    len_key : )doc";


 static const char *__doc_gr_radar_split_cc_split_cc = R"doc()doc";


 static const char *__doc_gr_radar_split_cc_make = R"doc(This block splits a tagged stream into segments. As packet_parts you give the structure of the packet, e.g. (10, 20, 5). With the packet number you can choose which packet shall be pushed to output. Counting begins on zero. E.g. packet_num=1 returns 20 items.

Constructor Specific Documentation:

Return a shared_ptr to a new instance of radar::split_cc.

To avoid accidental use of raw pointers, radar::split_cc's constructor is in a private implementation class. radar::split_cc::make is the public interface for creating new instances.

Args:
    packet_num : 
    packet_parts : 
    len_key : )doc";

  
