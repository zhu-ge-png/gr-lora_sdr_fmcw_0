#ifndef INCLUDED_LORA_SDR_FMCW_0_FRAME_ID_TRACKER_H
#define INCLUDED_LORA_SDR_FMCW_0_FRAME_ID_TRACKER_H

#include <string>

namespace gr {
namespace lora_sdr_fmcw_0 {
namespace frame_id_tracker {

void log_tx(const std::string& message);
void log_rx(const std::string& message, bool crc_valid);

} // namespace frame_id_tracker
} // namespace lora_sdr_fmcw_0
} // namespace gr

#endif /* INCLUDED_LORA_SDR_FMCW_0_FRAME_ID_TRACKER_H */
