/* -*- c++ -*- */
/*
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_LORA_SDR_FMCW_0_RADAR_RX0_H
#define INCLUDED_LORA_SDR_FMCW_0_RADAR_RX0_H

#include <gnuradio/block.h>
#include <gnuradio/lora_sdr_fmcw_0/api.h>
#include <string>

namespace gr {
namespace lora_sdr_fmcw_0 {

/*!
 * \brief Correlation-threshold FMCW radar receiver working on full triangle windows.
 * \ingroup lora_sdr
 */
class LORA_SDR_API radar_rx0 : virtual public gr::block
{
public:
    typedef std::shared_ptr<radar_rx0> sptr;

    /*!
     * \brief Create a radar receiver for LoRa-aligned FMCW triangles.
     *
     * Each detection decision is made on one complete FMCW triangle
     * (up-chirp + down-chirp), i.e. two LoRa symbol lengths.
     */
    static sptr make(uint32_t bandwidth,
                     uint8_t sf,
                     uint8_t os_factor = 4,
                     float corr_threshold = 0.45f,
                     const std::string& len_tag_key = "radar_len");

    virtual void set_corr_threshold(float corr_threshold) = 0;
};

} // namespace lora_sdr_fmcw_0
} // namespace gr

#endif /* INCLUDED_LORA_SDR_FMCW_0_RADAR_RX0_H */
