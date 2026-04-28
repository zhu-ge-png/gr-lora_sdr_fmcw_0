#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# GNU Radio version: 3.10.11.0

from gnuradio import blocks
import pmt
from gnuradio import channels
from gnuradio import gr
import sys
import signal
from gnuradio import radar
import gnuradio.lora_sdr_fmcw_0 as lora_sdr
import threading


class lora_fmcw_0_test1_add_channel_only(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        self.flowgraph_started = threading.Event()

        ##################################################
        # Variables
        ##################################################
        self.bw = bw = 125000
        self.sync_word = sync_word = 0x12
        self.soft_decoding = soft_decoding = False
        self.sf = sf = 7
        self.samp_rate = samp_rate = bw * 4
        self.preamb_len = preamb_len = 8
        self.pay_len = pay_len = 255
        self.min_out_buffer = min_out_buffer = 4096
        self.max_out_buffer = max_out_buffer = 0
        self.impl_head = impl_head = False
        self.has_crc = has_crc = True
        self.frame_period = frame_period = 2000
        self.fmcw_up_len = fmcw_up_len = 205
        self.fmcw_freq_sweep = fmcw_freq_sweep = 0.90 * bw
        self.fmcw_freq_cw = fmcw_freq_cw = -0.45 * bw
        self.fmcw_down_len = fmcw_down_len = 205
        self.fmcw_cw_len = fmcw_cw_len = 102
        self.decim_fac = decim_fac = 2**5
        self.cr = cr = 2
        self.corr_threshold = corr_threshold = 0.29
        self.clk_offset = clk_offset = 1
        self.center_freq = center_freq = 5800e6
        self.SNRdB = SNRdB = -7
        self.channel_startup_guard = channel_startup_guard = preamb_len * 2 * int((2**sf) * samp_rate / bw)

        ##################################################
        # Blocks
        ##################################################
        self.radar_signal_generator_fmcw_c_0 = radar.signal_generator_fmcw_c(
            samp_rate,
            fmcw_up_len,
            fmcw_down_len,
            fmcw_cw_len,
            fmcw_freq_cw,
            fmcw_freq_sweep,
            1,
            preamb_len,
            "frame_len",
            7,
            125000
        )
        self.blocks_tag_debug_fmcw0 = blocks.tag_debug(gr.sizeof_gr_complex, "fmcw0_tags", "frame_len")
        self.radar_signal_generator_fmcw_c_0.set_min_output_buffer(16384)
        self.lora_sdr_whitening_0_0 = lora_sdr.whitening(True, True, ',', 'packet_len')
        self.lora_sdr_payload_id_inc_0 = lora_sdr.payload_id_inc(':')
        self.lora_sdr_interleaver_0_0 = lora_sdr.interleaver(cr, sf, 0, bw)
        self.lora_sdr_header_decoder_0 = lora_sdr.header_decoder(impl_head, cr, pay_len, has_crc, 2, True)
        self.lora_sdr_header_0_0 = lora_sdr.header(impl_head, has_crc, cr)
        self.lora_sdr_hamming_enc_0_0 = lora_sdr.hamming_enc(cr, sf)
        self.lora_sdr_hamming_dec_0 = lora_sdr.hamming_dec(soft_decoding)
        self.lora_sdr_gray_mapping_0 = lora_sdr.gray_mapping(soft_decoding)
        self.lora_sdr_gray_demap_0_0 = lora_sdr.gray_demap(sf)
        self.lora_sdr_fmcw_0_modulate0_0 = lora_sdr.modulate0(sf, samp_rate, bw, [sync_word], 4096, preamb_len)
        self.lora_sdr_fmcw_0_modulate0_0.set_min_output_buffer(65536)
        self.lora_sdr_fmcw_0_frame_sync0_0 = lora_sdr.frame_sync0(center_freq, bw, sf, impl_head, [sync_word], 4, preamb_len, corr_threshold)
        self.lora_sdr_fft_demod_0 = lora_sdr.fft_demod(soft_decoding, False)
        self.lora_sdr_dewhitening_0 = lora_sdr.dewhitening()
        self.lora_sdr_deinterleaver_0 = lora_sdr.deinterleaver(soft_decoding)
        self.lora_sdr_crc_verif_0 = lora_sdr.crc_verif(1, False)
        self.lora_sdr_add_crc_0_0 = lora_sdr.add_crc(has_crc)
        self.channels_channel_model_0 = channels.channel_model(
            noise_voltage=(10**(-SNRdB/20)),
            frequency_offset=(center_freq*clk_offset*1e-6/samp_rate),
            epsilon=(1.0+clk_offset*1e-6),
            taps=[1.0 + 0.0j],
            noise_seed=0,
            block_tags=True)
        self.channels_channel_model_0.set_min_output_buffer((int((2**sf+2)*samp_rate/bw)))
        self.blocks_throttle2_0 = blocks.throttle(
            gr.sizeof_gr_complex * 1,
            samp_rate,
            True,
            0 if "auto" == "auto" else max(int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1),
        )
        self.blocks_delay_0 = blocks.delay(gr.sizeof_gr_complex * 1, channel_startup_guard)
        self.blocks_tagged_stream_mux_0 = blocks.tagged_stream_mux(gr.sizeof_gr_complex * 1, 'frame_len', 0)
        self.blocks_tagged_stream_mux_0.set_min_output_buffer(2097152)
        self.blocks_message_strobe_0_0_0 = blocks.message_strobe(pmt.intern("helloworld : 0"), frame_period)
        self.blocks_message_debug_strobe = blocks.message_debug()
        self.blocks_message_debug_inc = blocks.message_debug()

        self.blocks_tag_debug_mod0 = blocks.tag_debug(gr.sizeof_gr_complex, "mod0_tags", "")
        self.blocks_tag_debug_mux0 = blocks.tag_debug(gr.sizeof_gr_complex, "mux0_tags", "")

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_message_strobe_0_0_0, 'strobe'), (self.lora_sdr_payload_id_inc_0, 'msg_in'))
        self.msg_connect((self.blocks_message_strobe_0_0_0, 'strobe'), (self.lora_sdr_whitening_0_0, 'msg'))
        self.msg_connect((self.lora_sdr_header_decoder_0, 'frame_info'), (self.lora_sdr_fmcw_0_frame_sync0_0, 'frame_info'))
        self.msg_connect((self.lora_sdr_payload_id_inc_0, 'msg_out'), (self.blocks_message_strobe_0_0_0, 'set_msg'))
        self.connect((self.blocks_throttle2_0, 0), (self.blocks_delay_0, 0))
        self.connect((self.blocks_delay_0, 0), (self.channels_channel_model_0, 0))
        self.connect((self.channels_channel_model_0, 0), (self.lora_sdr_fmcw_0_frame_sync0_0, 0))
        self.connect((self.lora_sdr_add_crc_0_0, 0), (self.lora_sdr_hamming_enc_0_0, 0))
        self.connect((self.lora_sdr_deinterleaver_0, 0), (self.lora_sdr_hamming_dec_0, 0))
        self.connect((self.lora_sdr_dewhitening_0, 0), (self.lora_sdr_crc_verif_0, 0))
        self.connect((self.lora_sdr_fft_demod_0, 0), (self.lora_sdr_gray_mapping_0, 0))
        self.connect((self.lora_sdr_fmcw_0_frame_sync0_0, 0), (self.lora_sdr_fft_demod_0, 0))
        self.connect((self.lora_sdr_fmcw_0_modulate0_0, 0), (self.blocks_tagged_stream_mux_0, 1))
        self.connect((self.lora_sdr_gray_demap_0_0, 0), (self.lora_sdr_fmcw_0_modulate0_0, 0))
        self.connect((self.lora_sdr_gray_mapping_0, 0), (self.lora_sdr_deinterleaver_0, 0))
        self.connect((self.lora_sdr_hamming_dec_0, 0), (self.lora_sdr_header_decoder_0, 0))
        self.connect((self.lora_sdr_hamming_enc_0_0, 0), (self.lora_sdr_interleaver_0_0, 0))
        self.connect((self.lora_sdr_header_0_0, 0), (self.lora_sdr_add_crc_0_0, 0))
        self.connect((self.lora_sdr_header_decoder_0, 0), (self.lora_sdr_dewhitening_0, 0))
        self.connect((self.lora_sdr_interleaver_0_0, 0), (self.lora_sdr_gray_demap_0_0, 0))
        self.connect((self.lora_sdr_whitening_0_0, 0), (self.lora_sdr_header_0_0, 0))
        self.connect((self.radar_signal_generator_fmcw_c_0, 0), (self.blocks_tagged_stream_mux_0, 0))
        self.connect((self.blocks_tagged_stream_mux_0, 0), (self.blocks_throttle2_0, 0))
        self.msg_connect((self.blocks_message_strobe_0_0_0, 'strobe'),
                 (self.blocks_message_debug_strobe, 'print'))

        self.msg_connect((self.lora_sdr_payload_id_inc_0, 'msg_out'),
                 (self.blocks_message_debug_inc, 'print'))

        self.connect((self.lora_sdr_fmcw_0_modulate0_0, 0),
             (self.blocks_tag_debug_mod0, 0))

        self.connect((self.blocks_tagged_stream_mux_0, 0),
             (self.blocks_tag_debug_mux0, 0))

        self.connect((self.radar_signal_generator_fmcw_c_0, 0),
             (self.blocks_tag_debug_fmcw0, 0))

    def get_bw(self):
        return self.bw

    def set_bw(self, bw):
        self.bw = bw
        self.set_fmcw_freq_cw(-0.45 * self.bw)
        self.set_fmcw_freq_sweep(0.90 * self.bw)
        self.set_samp_rate(self.bw * 4)

    def get_sync_word(self):
        return self.sync_word

    def set_sync_word(self, sync_word):
        self.sync_word = sync_word

    def get_soft_decoding(self):
        return self.soft_decoding

    def set_soft_decoding(self, soft_decoding):
        self.soft_decoding = soft_decoding

    def get_sf(self):
        return self.sf

    def set_sf(self, sf):
        self.sf = sf
        self.lora_sdr_gray_demap_0_0.set_sf(self.sf)
        self.lora_sdr_hamming_enc_0_0.set_sf(self.sf)
        self.lora_sdr_interleaver_0_0.set_sf(self.sf)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle2_0.set_sample_rate(self.samp_rate)
        self.channels_channel_model_0.set_frequency_offset((self.center_freq*self.clk_offset*1e-6/self.samp_rate))

    def get_preamb_len(self):
        return self.preamb_len

    def set_preamb_len(self, preamb_len):
        self.preamb_len = preamb_len

    def get_pay_len(self):
        return self.pay_len

    def set_pay_len(self, pay_len):
        self.pay_len = pay_len

    def get_min_out_buffer(self):
        return self.min_out_buffer

    def set_min_out_buffer(self, min_out_buffer):
        self.min_out_buffer = min_out_buffer

    def get_max_out_buffer(self):
        return self.max_out_buffer

    def set_max_out_buffer(self, max_out_buffer):
        self.max_out_buffer = max_out_buffer

    def get_impl_head(self):
        return self.impl_head

    def set_impl_head(self, impl_head):
        self.impl_head = impl_head

    def get_has_crc(self):
        return self.has_crc

    def set_has_crc(self, has_crc):
        self.has_crc = has_crc

    def get_frame_period(self):
        return self.frame_period

    def set_frame_period(self, frame_period):
        self.frame_period = frame_period
        self.blocks_message_strobe_0_0_0.set_period(self.frame_period)

    def get_fmcw_up_len(self):
        return self.fmcw_up_len

    def set_fmcw_up_len(self, fmcw_up_len):
        self.fmcw_up_len = fmcw_up_len

    def get_fmcw_freq_sweep(self):
        return self.fmcw_freq_sweep

    def set_fmcw_freq_sweep(self, fmcw_freq_sweep):
        self.fmcw_freq_sweep = fmcw_freq_sweep

    def get_fmcw_freq_cw(self):
        return self.fmcw_freq_cw

    def set_fmcw_freq_cw(self, fmcw_freq_cw):
        self.fmcw_freq_cw = fmcw_freq_cw

    def get_fmcw_down_len(self):
        return self.fmcw_down_len

    def set_fmcw_down_len(self, fmcw_down_len):
        self.fmcw_down_len = fmcw_down_len

    def get_fmcw_cw_len(self):
        return self.fmcw_cw_len

    def set_fmcw_cw_len(self, fmcw_cw_len):
        self.fmcw_cw_len = fmcw_cw_len

    def get_decim_fac(self):
        return self.decim_fac

    def set_decim_fac(self, decim_fac):
        self.decim_fac = decim_fac

    def get_cr(self):
        return self.cr

    def set_cr(self, cr):
        self.cr = cr
        self.lora_sdr_hamming_enc_0_0.set_cr(self.cr)
        self.lora_sdr_header_0_0.set_cr(self.cr)
        self.lora_sdr_interleaver_0_0.set_cr(self.cr)

    def get_corr_threshold(self):
        return self.corr_threshold

    def set_corr_threshold(self, corr_threshold):
        self.corr_threshold = corr_threshold
        self.lora_sdr_fmcw_0_frame_sync0_0.set_detect_corr_threshold(self.corr_threshold)

    def get_clk_offset(self):
        return self.clk_offset

    def set_clk_offset(self, clk_offset):
        self.clk_offset = clk_offset
        self.channels_channel_model_0.set_frequency_offset((self.center_freq*self.clk_offset*1e-6/self.samp_rate))
        self.channels_channel_model_0.set_timing_offset((1.0+self.clk_offset*1e-6))

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.channels_channel_model_0.set_frequency_offset((self.center_freq*self.clk_offset*1e-6/self.samp_rate))

    def get_SNRdB(self):
        return self.SNRdB

    def set_SNRdB(self, SNRdB):
        self.SNRdB = SNRdB
        self.channels_channel_model_0.set_noise_voltage((10**(-self.SNRdB/20)))


def main(top_block_cls=lora_fmcw_0_test1_add_channel_only, options=None):
    tb = top_block_cls()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()
        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()
    tb.flowgraph_started.set()

    import time

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass

    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
