/* -*- c++ -*- */
/*
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_LORA_SDR_FMCW_0_RADAR_RX0_IMPL_H
#define INCLUDED_LORA_SDR_FMCW_0_RADAR_RX0_IMPL_H

#include <gnuradio/io_signature.h>
#include <gnuradio/lora_sdr_fmcw_0/radar_rx0.h>
#include <gnuradio/lora_sdr_fmcw_0/utilities.h>
#include <pmt/pmt.h>
#include <vector>

namespace gr {
namespace lora_sdr_fmcw_0 {

class radar_rx0_impl : public radar_rx0
{
private:
    uint32_t m_bw;
    uint8_t m_sf;
    uint8_t m_os_factor;
    uint32_t m_samples_per_symbol;
    uint32_t m_triangle_samples;

    float m_corr_threshold;
    bool m_locked;

    std::vector<gr_complex> m_triangle_template;
    float m_triangle_template_energy;

    pmt::pmt_t m_len_tag_key;
    pmt::pmt_t m_corr_tag_key;
    pmt::pmt_t m_srcid;

    void rebuild_triangle_template();
    float normalized_corr(const gr_complex* in) const;

public:
    radar_rx0_impl(uint32_t bandwidth,
                   uint8_t sf,
                   uint8_t os_factor,
                   float corr_threshold,
                   const std::string& len_tag_key);
    ~radar_rx0_impl() override;

    void set_corr_threshold(float corr_threshold) override;
    void forecast(int noutput_items, gr_vector_int& ninput_items_required) override;

    int general_work(int noutput_items,
                     gr_vector_int& ninput_items,
                     gr_vector_const_void_star& input_items,
                     gr_vector_void_star& output_items) override;
};

} // namespace lora_sdr_fmcw_0
} // namespace gr

#endif /* INCLUDED_LORA_SDR_FMCW_0_RADAR_RX0_IMPL_H */
