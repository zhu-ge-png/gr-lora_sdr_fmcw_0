/* -*- c++ -*- */
/*
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_LORA_SDR_FMCW_0_RADAR_ESTIMATOR_UPDOWN0_IMPL_H
#define INCLUDED_LORA_SDR_FMCW_0_RADAR_ESTIMATOR_UPDOWN0_IMPL_H

#include <gnuradio/lora_sdr_fmcw_0/radar_estimator_updown0.h>
#include <pmt/pmt.h>

namespace gr {
namespace lora_sdr_fmcw_0 {

class radar_estimator_updown0_impl : public radar_estimator_updown0
{
private:
    static constexpr float c_light = 299792458.0f;

    int m_samp_rate;
    float m_center_freq;
    float m_sweep_freq;
    int m_samp_up;
    int m_samp_down;
    bool m_push_power;

    float m_const_doppler;
    float m_const_up;
    float m_const_down;

    bool m_msg_up_in;
    bool m_msg_down_in;
    pmt::pmt_t m_msg_up;
    pmt::pmt_t m_msg_down;

    pmt::pmt_t m_port_id_in_up;
    pmt::pmt_t m_port_id_in_down;
    pmt::pmt_t m_port_id_out;

    void handle_msg_up(pmt::pmt_t msg);
    void handle_msg_down(pmt::pmt_t msg);
    void estimate();

public:
    radar_estimator_updown0_impl(int samp_rate,
                                 float center_freq,
                                 float sweep_freq,
                                 int samp_up,
                                 int samp_down,
                                 bool push_power);
    ~radar_estimator_updown0_impl() override;
};

} // namespace lora_sdr_fmcw_0
} // namespace gr

#endif /* INCLUDED_LORA_SDR_FMCW_0_RADAR_ESTIMATOR_UPDOWN0_IMPL_H */
