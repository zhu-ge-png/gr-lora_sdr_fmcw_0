/* -*- c++ -*- */
/* 
 * Copyright 2022 Tapparel Joachim @EPFL,TCL.
 * 
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 * 
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */


#ifndef INCLUDED_LORA_SDR_MODULATE_H
#define INCLUDED_LORA_SDR_MODULATE_H

#include <gnuradio/lora_sdr_fmcw_0/api.h>
#include <gnuradio/block.h>

namespace gr {
  namespace lora_sdr_fmcw_0 {

    /*!
     * \brief <+description of block+>
     * \ingroup lora_sdr
     *
     */
    class LORA_SDR_API modulate0 : virtual public gr::block
    {
     public:
      typedef std::shared_ptr<modulate0> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of lora_sdr::modulate0.
       *
       * To avoid accidental use of raw pointers, lora_sdr::modulate0's
       * constructor is in a private implementation
       * class. lora_sdr::modulate0::make is the public interface for
       * creating new instances.
       */
      static sptr make(uint8_t sf,
                       uint32_t samp_rate,
                       uint32_t bw,
                       std::vector<uint16_t> sync_words,
                       uint32_t inter_frame_padd,
                       uint16_t preamble_len,
                       uint16_t zero_preamble_chirps = 0);
    };

  } // namespace lora_sdr
} // namespace gr

#endif /* INCLUDED_LORA_SDR_MODULATE_H */
