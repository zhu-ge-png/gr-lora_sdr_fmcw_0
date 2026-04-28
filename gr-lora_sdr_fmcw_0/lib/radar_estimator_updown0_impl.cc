/* -*- c++ -*- */
/*
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include "radar_estimator_updown0_impl.h"

#include <gnuradio/io_signature.h>
#include <algorithm>
#include <cmath>
#include <limits>
#include <vector>

namespace gr {
namespace lora_sdr_fmcw_0 {

radar_estimator_updown0::sptr radar_estimator_updown0::make(int samp_rate,
                                                            float center_freq,
                                                            float sweep_freq,
                                                            int samp_up,
                                                            int samp_down,
                                                            bool push_power)
{
    return gnuradio::get_initial_sptr(new radar_estimator_updown0_impl(
        samp_rate, center_freq, sweep_freq, samp_up, samp_down, push_power));
}

radar_estimator_updown0_impl::radar_estimator_updown0_impl(int samp_rate,
                                                           float center_freq,
                                                           float sweep_freq,
                                                           int samp_up,
                                                           int samp_down,
                                                           bool push_power)
    : gr::block("radar_estimator_updown0",
                gr::io_signature::make(0, 0, 0),
                gr::io_signature::make(0, 0, 0)),
      m_samp_rate(std::max(1, samp_rate)),
      m_center_freq(std::max(center_freq, 1.0f)),
      m_sweep_freq(std::max(sweep_freq, 1.0f)),
      m_samp_up(std::max(1, samp_up)),
      m_samp_down(std::max(1, samp_down)),
      m_push_power(push_power),
      m_const_doppler(2.0f * m_center_freq / c_light),
      m_const_up(2.0f * m_sweep_freq / c_light * static_cast<float>(m_samp_rate) /
                 static_cast<float>(m_samp_up)),
      m_const_down(2.0f * m_sweep_freq / c_light * static_cast<float>(m_samp_rate) /
                   static_cast<float>(m_samp_down)),
      m_msg_up_in(false),
      m_msg_down_in(false)
{
    m_port_id_in_up = pmt::mp("Msg in UP");
    message_port_register_in(m_port_id_in_up);
    set_msg_handler(m_port_id_in_up,
                    [this](pmt::pmt_t msg) { this->handle_msg_up(msg); });

    m_port_id_in_down = pmt::mp("Msg in DOWN");
    message_port_register_in(m_port_id_in_down);
    set_msg_handler(m_port_id_in_down,
                    [this](pmt::pmt_t msg) { this->handle_msg_down(msg); });

    m_port_id_out = pmt::mp("Msg out");
    message_port_register_out(m_port_id_out);
}

radar_estimator_updown0_impl::~radar_estimator_updown0_impl() {}

void radar_estimator_updown0_impl::handle_msg_up(pmt::pmt_t msg)
{
    m_msg_up = msg;
    m_msg_up_in = true;
    if (m_msg_up_in && m_msg_down_in) {
        m_msg_up_in = false;
        m_msg_down_in = false;
        estimate();
    }
}

void radar_estimator_updown0_impl::handle_msg_down(pmt::pmt_t msg)
{
    m_msg_down = msg;
    m_msg_down_in = true;
    if (m_msg_up_in && m_msg_down_in) {
        m_msg_up_in = false;
        m_msg_down_in = false;
        estimate();
    }
}

void radar_estimator_updown0_impl::estimate()
{
    std::vector<float> freq_up;
    std::vector<float> freq_down;
    std::vector<float> power_up;
    std::vector<float> power_down;
    pmt::pmt_t timestamp =
        pmt::list2(pmt::string_to_symbol("rx_time"),
                   pmt::make_tuple(pmt::from_uint64(0), pmt::from_double(-1.0)));

    auto parse_msg = [&](const pmt::pmt_t& msg,
                         std::vector<float>& freq,
                         std::vector<float>& power,
                         bool allow_timestamp) {
        for (int k = 0; k < pmt::length(msg); ++k) {
            const pmt::pmt_t part = pmt::nth(k, msg);
            const std::string key = pmt::symbol_to_string(pmt::nth(0, part));
            if (key == "frequency") {
                freq = pmt::f32vector_elements(pmt::nth(1, part));
            } else if (key == "power") {
                power = pmt::f32vector_elements(pmt::nth(1, part));
            } else if (allow_timestamp && key == "rx_time") {
                timestamp = pmt::list2(pmt::string_to_symbol("rx_time"), pmt::nth(1, part));
            }
        }
    };

    parse_msg(m_msg_up, freq_up, power_up, true);
    parse_msg(m_msg_down, freq_down, power_down, false);

    if (freq_up.empty() || freq_down.empty()) {
        return;
    }

    bool found_valid_pair = false;
    bool found_any_pair = false;
    float best_range = 0.0f;
    float best_velocity = 0.0f;
    float best_power = 0.0f;
    float best_score = -std::numeric_limits<float>::infinity();
    float fallback_range = 0.0f;
    float fallback_velocity = 0.0f;
    float fallback_power = 0.0f;
    float fallback_score = -std::numeric_limits<float>::infinity();

    for (size_t m = 0; m < freq_up.size(); ++m) {
        for (size_t n = 0; n < freq_down.size(); ++n) {
            const float r = (freq_up[m] - freq_down[n]) / (m_const_up + m_const_down);
            const float v1 = (m_const_up * r - freq_up[m]) / m_const_doppler;
            const float v2 = (-m_const_down * r - freq_down[n]) / m_const_doppler;
            const float avg_velocity = (v1 + v2) * 0.5f;
            const float up_power = (m < power_up.size()) ? power_up[m] : 0.0f;
            const float down_power = (n < power_down.size()) ? power_down[n] : 0.0f;
            const float avg_power = 0.5f * (up_power + down_power);

            found_any_pair = true;
            if (avg_power > fallback_score) {
                fallback_score = avg_power;
                fallback_range = r;
                fallback_velocity = avg_velocity;
                fallback_power = avg_power;
            }

            if (r < 0.0f) {
                continue;
            }

            found_valid_pair = true;
            if (avg_power > best_score) {
                best_score = avg_power;
                best_range = r;
                best_velocity = avg_velocity;
                best_power = avg_power;
            }
        }
    }

    if (!found_any_pair) {
        return;
    }

    const float selected_range = found_valid_pair ? best_range : fallback_range;
    const float selected_velocity = found_valid_pair ? best_velocity : fallback_velocity;
    const float selected_power = found_valid_pair ? best_power : fallback_power;

    std::vector<float> range{ selected_range };
    std::vector<float> velocity{ selected_velocity };
    std::vector<float> power{ selected_power };

    pmt::pmt_t range_pack = pmt::list2(
        pmt::string_to_symbol("range"), pmt::init_f32vector(range.size(), range));
    pmt::pmt_t vel_pack = pmt::list2(
        pmt::string_to_symbol("velocity"),
        pmt::init_f32vector(velocity.size(), velocity));

    pmt::pmt_t out_msg;
    if (m_push_power) {
        pmt::pmt_t power_pack = pmt::list2(
            pmt::string_to_symbol("power"), pmt::init_f32vector(power.size(), power));
        out_msg = pmt::list4(timestamp, vel_pack, range_pack, power_pack);
    } else {
        out_msg = pmt::list3(timestamp, vel_pack, range_pack);
    }

    message_port_pub(m_port_id_out, out_msg);
}

} // namespace lora_sdr_fmcw_0
} // namespace gr
