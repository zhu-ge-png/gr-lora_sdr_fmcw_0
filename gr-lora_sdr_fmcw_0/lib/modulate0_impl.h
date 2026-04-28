#ifndef INCLUDED_LORA_FMCW_0_MODULATE0_IMPL_H
#define INCLUDED_LORA_FMCW_0_MODULATE0_IMPL_H

#include <gnuradio/lora_sdr_fmcw_0/modulate0.h>
#include <gnuradio/io_signature.h>
#include <iostream>
#include <fstream>

#include <gnuradio/lora_sdr_fmcw_0/utilities.h>

// #define GR_LORA_PRINT_INFO

namespace gr {
  namespace lora_sdr_fmcw_0 {

    class modulate0_impl : public modulate0
    {
     private:
        uint8_t m_sf; ///< Transmission spreading factor
        uint32_t m_samp_rate; ///< Transmission sampling rate
        uint32_t m_bw; ///< Transmission bandwidth (Works only for samp_rate=bw)
        uint32_t m_number_of_bins; ///< number of bin per LoRa symbol
        int m_samples_per_symbol; ///< samples per symbols (Works only for 2^sf)
        std::vector<uint16_t> m_sync_words; ///< sync words (network id)

        int m_ninput_items_required; ///< number of samples required to call this block (forecast)

        int m_os_factor; ///< oversampling factor based on sampling rate and bandwidth

        uint32_t m_inter_frame_padding; ///< length in samples of zero append to each frame

        int m_frame_len; ///< length of the frame in number of items

        std::vector<gr_complex> m_upchirp;   ///< reference upchirp
        std::vector<gr_complex> m_downchirp; ///< reference downchirp

        // In the FMCW-0 design, the radar branch can provide part of the preamble.
        uint16_t m_preamb_len; ///< total number of preamble upchirp units
        uint16_t m_zero_preamble_chirps; ///< number of 0-bin LoRa upchirps kept before sync words
        int32_t samp_cnt;      ///< counter of the number of LoRa samples sent
        int32_t preamb_samp_cnt; ///< counter of the number of sync-tail samples output
        uint32_t padd_cnt;     ///< counter of the number of null samples output after each frame
        uint64_t frame_cnt;    ///< counter of the number of frames sent
        bool frame_end;        ///< indicate that we sent a full frame

        tag_t m_config_tag;
        tag_t m_framelen_tag;

     public:
      modulate0_impl(uint8_t sf, uint32_t samp_rate, uint32_t bw, std::vector<uint16_t> sync_words, uint32_t frame_zero_padd, uint16_t preamb_len, uint16_t zero_preamble_chirps = 0);
      ~modulate0_impl();

      void set_sf(uint8_t sf);

      // Where all the action really happens
      void forecast (int noutput_items, gr_vector_int &ninput_items_required);
      void update_var(int new_sf, int new_bw);
      int general_work(int noutput_items,
           gr_vector_int &ninput_items,
           gr_vector_const_void_star &input_items,
           gr_vector_void_star &output_items);
    };

  } // namespace lora_sdr_fmcw_0
} // namespace gr

#endif /* INCLUDED_LORA_FMCW_0_MODULATE0_IMPL_H */
