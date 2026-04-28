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

#ifndef INCLUDED_RADAR_SIGNAL_GENERATOR_FMCW_C_IMPL_H
#define INCLUDED_RADAR_SIGNAL_GENERATOR_FMCW_C_IMPL_H

#include <complex>
#include <vector>
#include <radar/signal_generator_fmcw_c.h>

namespace gr {
namespace radar {

class signal_generator_fmcw_c_impl : public signal_generator_fmcw_c
{
public:
    signal_generator_fmcw_c_impl(const int samp_rate,
                                 const int samp_up,
                                 const int samp_down,
                                 const int samp_cw,
                                 const float freq_cw,
                                 const float freq_sweep,
                                 const float amplitude,
                                 const int repeat_count,
                                 const std::string& len_key,
                                 const int lora_sf,
                                 const float lora_bw);
    ~signal_generator_fmcw_c_impl() override;

    int work(int noutput_items,
             gr_vector_const_void_star& input_items,
             gr_vector_void_star& output_items) override;

private:
    const int d_samp_rate;
    const int d_req_samp_up;
    const int d_req_samp_down;
    const int d_req_samp_cw;
    const int d_lora_sf;
    const float d_lora_bw;
    const bool d_use_lora_timing;

    const int d_legacy_cw_len;
    const int d_triangle_up_len;
    const int d_triangle_down_len;
    const int d_symbol_len;
    const int d_repeat_count;
    const int d_packet_len;

    const float d_freq_cw;
    const float d_freq_sweep;
    const float d_amplitude;

    const pmt::pmt_t d_key_len;
    const pmt::pmt_t d_value_len;
    const pmt::pmt_t d_srcid;

    std::complex<float> d_phase;
    std::vector<float> d_waveform;
    int d_wv_counter;

    void build_legacy_waveform();
    void build_lora_aligned_waveform();
    void fill_linear_ramp(int start_idx, int length, float start_freq, float stop_freq);
};

} // namespace radar
} // namespace gr

#endif /* INCLUDED_RADAR_SIGNAL_GENERATOR_FMCW_C_IMPL_H */
