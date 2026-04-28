/* -*- c++ -*- */
/*
 * Copyright 2014 Communications Engineering Lab, KIT.
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

#ifndef INCLUDED_RADAR_SIGNAL_GENERATOR_FMCW_C_H
#define INCLUDED_RADAR_SIGNAL_GENERATOR_FMCW_C_H

#include <gnuradio/sync_block.h>
#include <radar/api.h>

namespace gr {
namespace radar {

/*! Generates a baseband FMCW waveform.
 *
 * Legacy mode keeps the original FMCW semantics:
 *
 * 1. CW part with constant frequency
 * 2. Up-chirp
 * 3. Down-chirp
 *
 * The packet length for tagged streams is the single-waveform length times
 * repeat_count.
 *
 * When lora_sf > 0 and lora_bw > 0, the block switches to a LoRa-aligned
 * triangle mode:
 *
 * 1. No CW section is emitted
 * 2. The up-sweep duration is 2^SF / BW seconds
 * 3. The down-sweep duration is 2^SF / BW seconds
 * 4. repeat_count selects how many triangles are generated per tagged packet
 *
 * In LoRa-aligned mode, the complex baseband sweep spans -BW/2 to +BW/2 so
 * that it matches the chirp range produced by the LoRa modulator.
 *
 * \ingroup radar
 */
class RADAR_API signal_generator_fmcw_c : virtual public gr::sync_block
{
public:
    typedef std::shared_ptr<signal_generator_fmcw_c> sptr;

    /*!
     * \param samp_rate Signal sample rate (samples per second)
     * \param samp_up Number samples of up-chirp part
     * \param samp_down Number samples of down-chirp part
     * \param samp_cw Number samples of CW part
     * \param freq_cw CW signal frequency in baseband
     * \param freq_sweep Sweep frequency of up- and down-chirp
     * \param amplitude Signal amplitude
     * \param repeat_count Number of waveform repetitions per tagged packet
     * \param len_key Packet length key for tagged stream
     * \param lora_sf Optional spreading factor for LoRa-aligned triangle mode
     * \param lora_bw Optional bandwidth for LoRa-aligned triangle mode (Hz)
     */
    static sptr make(const int samp_rate,
                     const int samp_up,
                     const int samp_down,
                     const int samp_cw,
                     const float freq_cw,
                     const float freq_sweep,
                     const float amplitude,
                     const int repeat_count = 1,
                     const std::string& len_key = "packet_len",
                     const int lora_sf = 0,
                     const float lora_bw = 0.0f);
};

} // namespace radar
} // namespace gr

#endif /* INCLUDED_RADAR_SIGNAL_GENERATOR_FMCW_C_H */
