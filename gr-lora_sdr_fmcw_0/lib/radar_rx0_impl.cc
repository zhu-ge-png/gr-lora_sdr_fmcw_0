/* -*- c++ -*- */
/*
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include "radar_rx0_impl.h"

#include <algorithm>
#include <cmath>
#include <cstring>

namespace gr {
namespace lora_sdr_fmcw_0 {

namespace {

float compute_energy(const std::vector<gr_complex>& samples)
{
    float energy = 0.0f;
    for (const auto& sample : samples) {
        energy += std::norm(sample);
    }
    return std::max(energy, 1.0e-12f);
}

} // namespace

radar_rx0::sptr radar_rx0::make(uint32_t bandwidth,
                                uint8_t sf,
                                uint8_t os_factor,
                                float corr_threshold,
                                const std::string& len_tag_key)
{
    return gnuradio::get_initial_sptr(
        new radar_rx0_impl(bandwidth, sf, os_factor, corr_threshold, len_tag_key));
}

radar_rx0_impl::radar_rx0_impl(uint32_t bandwidth,
                               uint8_t sf,
                               uint8_t os_factor,
                               float corr_threshold,
                               const std::string& len_tag_key)
    : gr::block("radar_rx0",
                gr::io_signature::make(1, 1, sizeof(gr_complex)),
                gr::io_signature::make2(1, 2, sizeof(gr_complex), sizeof(float))),
      m_bw(std::max<uint32_t>(1u, bandwidth)),
      m_sf(sf),
      m_os_factor(std::max<uint8_t>(1, os_factor)),
      m_samples_per_symbol((1u << sf) * std::max<uint8_t>(1, os_factor)),
      m_triangle_samples(2u * (1u << sf) * std::max<uint8_t>(1, os_factor)),
      m_corr_threshold(std::clamp(corr_threshold, 0.0f, 1.0f)),
      m_locked(false),
      m_triangle_template(m_triangle_samples),
      m_triangle_template_energy(1.0f),
      m_len_tag_key(pmt::string_to_symbol(len_tag_key.empty() ? "radar_len" : len_tag_key)),
      m_corr_tag_key(pmt::string_to_symbol("radar_corr")),
      m_srcid(pmt::string_to_symbol("radar_rx0"))
{
    set_tag_propagation_policy(TPP_DONT);
    set_output_multiple(m_triangle_samples);
    rebuild_triangle_template();
}

radar_rx0_impl::~radar_rx0_impl() {}

void radar_rx0_impl::rebuild_triangle_template()
{
    std::vector<gr_complex> upchirp(m_samples_per_symbol);
    std::vector<gr_complex> downchirp(m_samples_per_symbol);

    build_ref_chirps(&upchirp[0], &downchirp[0], m_sf, m_os_factor);

    std::memcpy(&m_triangle_template[0],
                &upchirp[0],
                m_samples_per_symbol * sizeof(gr_complex));
    std::memcpy(&m_triangle_template[m_samples_per_symbol],
                &downchirp[0],
                m_samples_per_symbol * sizeof(gr_complex));
    m_triangle_template_energy = compute_energy(m_triangle_template);
}

float radar_rx0_impl::normalized_corr(const gr_complex* in) const
{
    gr_complex dot(0.0f, 0.0f);
    float sig_energy = 0.0f;

    for (uint32_t i = 0; i < m_triangle_samples; ++i) {
        dot += in[i] * std::conj(m_triangle_template[i]);
        sig_energy += std::norm(in[i]);
    }

    const float denom =
        std::sqrt(std::max(sig_energy * m_triangle_template_energy, 1.0e-20f));
    return std::abs(dot) / denom;
}

void radar_rx0_impl::set_corr_threshold(float corr_threshold)
{
    m_corr_threshold = std::clamp(corr_threshold, 0.0f, 1.0f);
}

void radar_rx0_impl::forecast(int /*noutput_items*/, gr_vector_int& ninput_items_required)
{
    ninput_items_required[0] = static_cast<int>(m_triangle_samples);
}

int radar_rx0_impl::general_work(int noutput_items,
                                 gr_vector_int& ninput_items,
                                 gr_vector_const_void_star& input_items,
                                 gr_vector_void_star& output_items)
{
    const auto* in = static_cast<const gr_complex*>(input_items[0]);
    auto* out = static_cast<gr_complex*>(output_items[0]);
    auto* corr_out =
        (output_items.size() > 1 && output_items[1] != nullptr)
            ? static_cast<float*>(output_items[1])
            : nullptr;

    const int available = ninput_items[0];
    const int triangle = static_cast<int>(m_triangle_samples);

    int consumed = 0;
    int produced = 0;

    while ((available - consumed) >= triangle) {
        const float corr = normalized_corr(in + consumed);
        if (corr >= m_corr_threshold) {
            if ((produced + triangle) > noutput_items) {
                break;
            }

            std::memcpy(out + produced, in + consumed, triangle * sizeof(gr_complex));
            if (corr_out != nullptr) {
                std::fill(corr_out + produced, corr_out + produced + triangle, corr);
            }

            const uint64_t out_off = nitems_written(0) + static_cast<uint64_t>(produced);
            add_item_tag(0, out_off, m_len_tag_key, pmt::from_long(triangle), m_srcid);
            add_item_tag(0, out_off, m_corr_tag_key, pmt::from_double(corr), m_srcid);

            produced += triangle;
            consumed += triangle;
            m_locked = true;
            continue;
        }

        consumed += 1;
        m_locked = false;
    }

    consume_each(consumed);
    return produced;
}

} // namespace lora_sdr_fmcw_0
} // namespace gr
