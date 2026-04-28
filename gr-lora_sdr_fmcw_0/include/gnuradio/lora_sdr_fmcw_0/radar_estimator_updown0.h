/* -*- c++ -*- */
/*
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_LORA_SDR_FMCW_0_RADAR_ESTIMATOR_UPDOWN0_H
#define INCLUDED_LORA_SDR_FMCW_0_RADAR_ESTIMATOR_UPDOWN0_H

#include <gnuradio/block.h>
#include <gnuradio/lora_sdr_fmcw_0/api.h>

namespace gr {
namespace lora_sdr_fmcw_0 {

/*!
 * \brief Estimate FMCW range and velocity from up/down chirp peak messages only.
 * \ingroup lora_sdr
 */
class LORA_SDR_API radar_estimator_updown0 : virtual public gr::block
{
public:
    typedef std::shared_ptr<radar_estimator_updown0> sptr;

    static sptr make(int samp_rate,
                     float center_freq,
                     float sweep_freq,
                     int samp_up,
                     int samp_down,
                     bool push_power = false);
};

} // namespace lora_sdr_fmcw_0
} // namespace gr

#endif /* INCLUDED_LORA_SDR_FMCW_0_RADAR_ESTIMATOR_UPDOWN0_H */
