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

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include "signal_generator_fmcw_c_impl.h"
#include <gnuradio/io_signature.h>
#include <gnuradio/math.h>
#include <algorithm>
#include <cmath>
#include <iostream>

namespace gr {
namespace radar {

namespace {

int calc_lora_symbol_samples(const int samp_rate, const int sf, const float bw)
{
    if (samp_rate <= 0 || sf <= 0 || bw <= 0.0f) {
        return 0;
    }

    const double symbol_count = std::ldexp(1.0, sf);
    const double symbol_samples = symbol_count * static_cast<double>(samp_rate) / bw;
    return std::max(1, static_cast<int>(std::llround(symbol_samples)));
}

} // namespace

signal_generator_fmcw_c::sptr signal_generator_fmcw_c::make(const int samp_rate,
                                                            const int samp_up,
                                                            const int samp_down,
                                                            const int samp_cw,
                                                            const float freq_cw,
                                                            const float freq_sweep,
                                                            const float amplitude,
                                                            const int repeat_count,
                                                            const std::string& len_key,
                                                            const int lora_sf,
                                                            const float lora_bw)
{
    return gnuradio::make_block_sptr<signal_generator_fmcw_c_impl>(samp_rate,
                                                                   samp_up,
                                                                   samp_down,
                                                                   samp_cw,
                                                                   freq_cw,
                                                                   freq_sweep,
                                                                   amplitude,
                                                                   repeat_count,
                                                                   len_key,
                                                                   lora_sf,
                                                                   lora_bw);
}

signal_generator_fmcw_c_impl::signal_generator_fmcw_c_impl(const int samp_rate,
                                                           const int samp_up,
                                                           const int samp_down,
                                                           const int samp_cw,
                                                           const float freq_cw,
                                                           const float freq_sweep,
                                                           const float amplitude,
                                                           const int repeat_count,
                                                           const std::string& len_key,
                                                           const int lora_sf,
                                                           const float lora_bw)
    : gr::sync_block("signal_generator_fmcw_c",
                     gr::io_signature::make(0, 0, 0),
                     gr::io_signature::make(1, 1, sizeof(gr_complex))),
      d_samp_rate(std::max(1, samp_rate)),
      d_req_samp_up(std::max(0, samp_up)),
      d_req_samp_down(std::max(0, samp_down)),
      d_req_samp_cw(std::max(0, samp_cw)),
      d_lora_sf(std::max(0, lora_sf)),
      d_lora_bw(std::max(0.0f, lora_bw)),
      d_use_lora_timing(d_lora_sf > 0 && d_lora_bw > 0.0f),
      d_legacy_cw_len(d_use_lora_timing ? 0 : d_req_samp_cw),
      d_triangle_up_len(d_use_lora_timing ? calc_lora_symbol_samples(d_samp_rate, d_lora_sf, d_lora_bw)
                                          : d_req_samp_up),
      d_triangle_down_len(d_use_lora_timing ? calc_lora_symbol_samples(d_samp_rate, d_lora_sf, d_lora_bw)
                                            : d_req_samp_down),
      d_symbol_len(std::max(1, d_legacy_cw_len + d_triangle_up_len + d_triangle_down_len)),
      d_repeat_count(std::max(1, repeat_count)),
      d_packet_len(d_symbol_len * d_repeat_count),
      d_freq_cw(freq_cw),
      d_freq_sweep(freq_sweep),
      d_amplitude(amplitude),
      d_key_len(pmt::string_to_symbol(len_key)),
      d_value_len(pmt::from_long(d_packet_len)),
      d_srcid(pmt::string_to_symbol("signal_generator_fmcw_c")),
      d_phase(1.0f, 0.0f),
      d_waveform(d_symbol_len, d_use_lora_timing ? (-0.5f * d_lora_bw) : d_freq_cw),
      d_wv_counter(0)
{
    if (d_use_lora_timing) {
        build_lora_aligned_waveform();
        std::cerr << "[signal_generator_fmcw_c] LoRa-aligned triangle mode"
                  << " sf=" << d_lora_sf
                  << " bw=" << d_lora_bw
                  << " up_len=" << d_triangle_up_len
                  << " down_len=" << d_triangle_down_len
                  << " repeat_count=" << d_repeat_count
                  << " packet_len=" << d_packet_len
                  << std::endl;
    } else {
        build_legacy_waveform();
        std::cerr << "[signal_generator_fmcw_c] legacy FMCW mode"
                  << " cw_len=" << d_legacy_cw_len
                  << " up_len=" << d_triangle_up_len
                  << " down_len=" << d_triangle_down_len
                  << " repeat_count=" << d_repeat_count
                  << " packet_len=" << d_packet_len
                  << std::endl;
    }
}

signal_generator_fmcw_c_impl::~signal_generator_fmcw_c_impl() {}

void signal_generator_fmcw_c_impl::fill_linear_ramp(const int start_idx,
                                                    const int length,
                                                    const float start_freq,
                                                    const float stop_freq)
{
    if (length <= 0) {
        return;
    }

    if (length == 1) {
        d_waveform[start_idx] = start_freq;
        return;
    }

    const float denom = static_cast<float>(length - 1);
    for (int k = 0; k < length; ++k) {
        const float alpha = static_cast<float>(k) / denom;
        d_waveform[start_idx + k] = start_freq + (stop_freq - start_freq) * alpha;
    }
}

void signal_generator_fmcw_c_impl::build_legacy_waveform()
{
    std::fill(d_waveform.begin(), d_waveform.end(), d_freq_cw);

    int offset = d_legacy_cw_len;
    fill_linear_ramp(offset, d_triangle_up_len, d_freq_cw, d_freq_cw + d_freq_sweep);
    offset += d_triangle_up_len;
    fill_linear_ramp(offset, d_triangle_down_len, d_freq_cw + d_freq_sweep, d_freq_cw);
}

void signal_generator_fmcw_c_impl::build_lora_aligned_waveform()
{
    const float half_bw = d_lora_bw * 0.5f;
    fill_linear_ramp(0, d_triangle_up_len, -half_bw, half_bw);
    fill_linear_ramp(d_triangle_up_len, d_triangle_down_len, half_bw, -half_bw);
}

int signal_generator_fmcw_c_impl::work(int noutput_items,
                                       gr_vector_const_void_star& /*input_items*/,
                                       gr_vector_void_star& output_items)
{
    gr_complex* out = static_cast<gr_complex*>(output_items[0]);

    for (int i = 0; i < noutput_items; ++i) {
        const uint64_t abs_idx = nitems_written(0) + static_cast<uint64_t>(i);
        if ((abs_idx % static_cast<uint64_t>(d_packet_len)) == 0ULL) {
            add_item_tag(0, abs_idx, d_key_len, d_value_len, d_srcid);
            d_wv_counter = 0;
        }

        out[i] = d_amplitude * d_phase;

        const float phase_inc =
            2.0f * GR_M_PI * d_waveform[d_wv_counter] / static_cast<float>(d_samp_rate);
        d_phase *= std::exp(gr_complex(0.0f, phase_inc));

        d_wv_counter += 1;
        if (d_wv_counter >= d_symbol_len) {
            d_wv_counter = 0;
        }
    }

    return noutput_items;
}

} /* namespace radar */
} /* namespace gr */
