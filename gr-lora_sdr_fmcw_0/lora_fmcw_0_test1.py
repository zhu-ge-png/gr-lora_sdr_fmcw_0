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
from gnuradio import blocks, gr
from gnuradio import channels
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import radar
import gnuradio.lora_sdr_fmcw_0 as lora_sdr
import threading




class lora_fmcw_0_test1(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        self.flowgraph_started = threading.Event()

        ##################################################
        # Variables
        ##################################################
        self.sf = sf = 7
        self.samp_rate = samp_rate = 25000000
        self.preamb_len = preamb_len = 8
        self.capture_out_dir = capture_out_dir = "/tmp"
        self.bw = bw = 12500000
        self.sync_word = sync_word = 0x12
        self.soft_decoding = soft_decoding = False
        self.radar_target_velocity = radar_target_velocity = 0
        self.radar_target_rcs = radar_target_rcs = 1e16
        self.radar_target_range = radar_target_range = 75
        self.radar_self_coupling = radar_self_coupling = False
        self.radar_rx_capture_samples = radar_rx_capture_samples = preamb_len * 2 * int((2**sf) * samp_rate / bw)
        self.radar_rx_capture_path = radar_rx_capture_path = capture_out_dir + "/lora_fmcw_0_test1_radar_rx.dat"
        self.radar_peak_threshold = radar_peak_threshold = -120
        self.radar_peak_protect = radar_peak_protect = 1
        self.radar_half_chirp_samples = radar_half_chirp_samples = int((2**sf) * samp_rate / bw)
        self.radar_corr_threshold = radar_corr_threshold = 0.15
        self.pay_len = pay_len = 255
        self.os_factor = os_factor = int(samp_rate / bw)
        self.min_out_buffer = min_out_buffer = 262144
        self.max_out_buffer = max_out_buffer = 262144
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
        self.corr_threshold = corr_threshold = 0.25
        self.clk_offset = clk_offset = 1.5
        self.channel_startup_guard = channel_startup_guard = preamb_len * 2 * int((2**sf) * samp_rate / bw)
        self.center_freq = center_freq = 5800e6
        self.SNRdB = SNRdB = -7

        ##################################################
        # Blocks
        ##################################################

        self.radar_ts_fft_cc_0_0 = radar.ts_fft_cc(radar_half_chirp_samples, "radar_len")
        self.radar_ts_fft_cc_0 = radar.ts_fft_cc(radar_half_chirp_samples, "radar_len")
        self.radar_static_target_simulator_cc_0 = radar.static_target_simulator_cc([radar_target_range], [radar_target_velocity], [radar_target_rcs], [0], [0], samp_rate, center_freq, -10, True, radar_self_coupling, "radar_len")
        self.radar_static_target_simulator_cc_0.set_min_output_buffer(min_out_buffer)
        self.radar_split_cc_0_0 = radar.split_cc(1, [radar_half_chirp_samples,radar_half_chirp_samples], "radar_len")
        self.radar_split_cc_0 = radar.split_cc(0, [radar_half_chirp_samples,radar_half_chirp_samples], "radar_len")
        self.radar_signal_generator_fmcw_c_1 = radar.signal_generator_fmcw_c(samp_rate, fmcw_up_len, fmcw_down_len, fmcw_cw_len, fmcw_freq_cw, fmcw_freq_sweep, 1, 1, "radar_len", sf, bw)
        self.radar_signal_generator_fmcw_c_0 = radar.signal_generator_fmcw_c(samp_rate, fmcw_up_len, fmcw_down_len, fmcw_cw_len, fmcw_freq_cw, fmcw_freq_sweep, 1, preamb_len, "frame_len", sf, bw)
        self.radar_signal_generator_fmcw_c_0.set_min_output_buffer(16384)
        self.radar_print_results_0 = radar.print_results(False, "")
        self.radar_find_max_peak_c_0_0 = radar.find_max_peak_c(samp_rate, radar_peak_threshold, radar_peak_protect, [1,1], False, "radar_len")
        self.radar_find_max_peak_c_0 = radar.find_max_peak_c(samp_rate, radar_peak_threshold, radar_peak_protect, [1,1], False, "radar_len")
        self.lora_sdr_whitening_0_0 = lora_sdr.whitening(True,True,',','packet_len')
        self.lora_sdr_payload_id_inc_0 = lora_sdr.payload_id_inc(':')
        self.lora_sdr_interleaver_0_0 = lora_sdr.interleaver(cr, sf, 0, bw)
        self.lora_sdr_header_decoder_0 = lora_sdr.header_decoder(impl_head, cr, pay_len, has_crc, 2, True)
        self.lora_sdr_header_0_0 = lora_sdr.header(impl_head, has_crc, cr)
        self.lora_sdr_hamming_enc_0_0 = lora_sdr.hamming_enc(cr, sf)
        self.lora_sdr_hamming_dec_0 = lora_sdr.hamming_dec(soft_decoding)
        self.lora_sdr_gray_mapping_0 = lora_sdr.gray_mapping( soft_decoding)
        self.lora_sdr_gray_demap_0_0 = lora_sdr.gray_demap(sf)
        self.lora_sdr_fmcw_0_radar_rx0_0 = lora_sdr.radar_rx0(bw, sf, os_factor, radar_corr_threshold, "radar_len")
        self.lora_sdr_fmcw_0_radar_estimator_updown0_0 = lora_sdr.radar_estimator_updown0(samp_rate, center_freq, bw, radar_half_chirp_samples, radar_half_chirp_samples, False)
        self.lora_sdr_fmcw_0_modulate0_0 = lora_sdr.modulate0(sf, samp_rate, bw, [sync_word], 4096,preamb_len)
        self.lora_sdr_fmcw_0_modulate0_0.set_min_output_buffer(min_out_buffer)
        self.lora_sdr_fmcw_0_frame_sync0_0 = lora_sdr.frame_sync0(center_freq, bw, sf, impl_head, [sync_word], os_factor,preamb_len, corr_threshold)
        self.lora_sdr_fft_demod_0 = lora_sdr.fft_demod( soft_decoding, False)
        self.lora_sdr_dewhitening_0 = lora_sdr.dewhitening()
        self.lora_sdr_deinterleaver_0 = lora_sdr.deinterleaver( soft_decoding)
        self.lora_sdr_crc_verif_0 = lora_sdr.crc_verif( 1, False)
        self.lora_sdr_add_crc_0_0 = lora_sdr.add_crc(has_crc)
        self.channels_channel_model_0 = channels.channel_model(
            noise_voltage=(10**(-SNRdB/20)),
            frequency_offset=(center_freq*clk_offset*1e-6/samp_rate),
            epsilon=(1.0+clk_offset*1e-6),
            taps=[1.0 + 0.0j],
            noise_seed=0,
            block_tags=True)
        self.channels_channel_model_0.set_min_output_buffer((int((2**sf+2)*samp_rate/bw)))
        self.blocks_throttle2_0 = blocks.throttle( gr.sizeof_gr_complex*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_throttle2_0.set_min_output_buffer(min_out_buffer)
        self.blocks_tagged_stream_mux_0 = blocks.tagged_stream_mux(gr.sizeof_gr_complex*1, 'frame_len', 0)
        self.blocks_tagged_stream_mux_0.set_min_output_buffer(2097152)
        self.blocks_tag_debug_2 = blocks.tag_debug(gr.sizeof_gr_complex*1, 'radar_after_rx', "radar_len")
        self.blocks_tag_debug_2.set_display(False)
        self.blocks_tag_debug_1 = blocks.tag_debug(gr.sizeof_gr_complex*1, 'fmcw_before_mux', "frame_len")
        self.blocks_tag_debug_1.set_display(False)
        self.blocks_tag_debug_0 = blocks.tag_debug(gr.sizeof_gr_complex*1, 'lora_before_mux', "frame_len")
        self.blocks_tag_debug_0.set_display(False)
        self.blocks_null_sink_radar_rx_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_multiply_conjugate_cc_0 = blocks.multiply_conjugate_cc(1)
        self.blocks_message_strobe_0_0_0 = blocks.message_strobe(pmt.intern("helloworld : 0"), frame_period)
        self.blocks_message_debug_strobe = blocks.message_debug(True, gr.log_levels.info)
        self.blocks_message_debug_radar_up = blocks.message_debug(True, gr.log_levels.info)
        self.blocks_message_debug_radar_down = blocks.message_debug(True, gr.log_levels.info)
        self.blocks_message_debug_inc = blocks.message_debug(True, gr.log_levels.info)
        self.blocks_head_radar_rx_capture_0 = blocks.head(gr.sizeof_gr_complex*1, radar_rx_capture_samples)
        self.blocks_file_sink_radar_rx_capture_0 = blocks.file_sink(gr.sizeof_gr_complex*1, radar_rx_capture_path, False)
        self.blocks_file_sink_radar_rx_capture_0.set_unbuffered(True)
        self.blocks_delay_0 = blocks.delay(gr.sizeof_gr_complex*1, channel_startup_guard)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_message_strobe_0_0_0, 'strobe'), (self.blocks_message_debug_strobe, 'print'))
        self.msg_connect((self.blocks_message_strobe_0_0_0, 'strobe'), (self.lora_sdr_payload_id_inc_0, 'msg_in'))
        self.msg_connect((self.blocks_message_strobe_0_0_0, 'strobe'), (self.lora_sdr_whitening_0_0, 'msg'))
        self.msg_connect((self.lora_sdr_fmcw_0_radar_estimator_updown0_0, 'Msg out'), (self.radar_print_results_0, 'Msg in'))
        self.msg_connect((self.lora_sdr_header_decoder_0, 'frame_info'), (self.lora_sdr_fmcw_0_frame_sync0_0, 'frame_info'))
        self.msg_connect((self.lora_sdr_payload_id_inc_0, 'msg_out'), (self.blocks_message_debug_inc, 'print'))
        self.msg_connect((self.lora_sdr_payload_id_inc_0, 'msg_out'), (self.blocks_message_strobe_0_0_0, 'set_msg'))
        self.msg_connect((self.radar_find_max_peak_c_0, 'Msg out'), (self.blocks_message_debug_radar_up, 'print'))
        self.msg_connect((self.radar_find_max_peak_c_0, 'Msg out'), (self.lora_sdr_fmcw_0_radar_estimator_updown0_0, 'Msg in UP'))
        self.msg_connect((self.radar_find_max_peak_c_0_0, 'Msg out'), (self.blocks_message_debug_radar_down, 'print'))
        self.msg_connect((self.radar_find_max_peak_c_0_0, 'Msg out'), (self.lora_sdr_fmcw_0_radar_estimator_updown0_0, 'Msg in DOWN'))
        self.connect((self.blocks_delay_0, 0), (self.channels_channel_model_0, 0))
        self.connect((self.blocks_head_radar_rx_capture_0, 0), (self.blocks_file_sink_radar_rx_capture_0, 0))
        self.connect((self.blocks_multiply_conjugate_cc_0, 0), (self.radar_split_cc_0, 0))
        self.connect((self.blocks_multiply_conjugate_cc_0, 0), (self.radar_split_cc_0_0, 0))
        self.connect((self.blocks_tagged_stream_mux_0, 0), (self.blocks_throttle2_0, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.blocks_delay_0, 0))
        self.connect((self.channels_channel_model_0, 0), (self.lora_sdr_fmcw_0_frame_sync0_0, 0))
        self.connect((self.lora_sdr_add_crc_0_0, 0), (self.lora_sdr_hamming_enc_0_0, 0))
        self.connect((self.lora_sdr_deinterleaver_0, 0), (self.lora_sdr_hamming_dec_0, 0))
        self.connect((self.lora_sdr_dewhitening_0, 0), (self.lora_sdr_crc_verif_0, 0))
        self.connect((self.lora_sdr_fft_demod_0, 0), (self.lora_sdr_gray_mapping_0, 0))
        self.connect((self.lora_sdr_fmcw_0_frame_sync0_0, 0), (self.lora_sdr_fft_demod_0, 0))
        self.connect((self.lora_sdr_fmcw_0_modulate0_0, 0), (self.blocks_tag_debug_0, 0))
        self.connect((self.lora_sdr_fmcw_0_modulate0_0, 0), (self.blocks_tagged_stream_mux_0, 1))
        self.connect((self.lora_sdr_fmcw_0_radar_rx0_0, 0), (self.blocks_head_radar_rx_capture_0, 0))
        self.connect((self.lora_sdr_fmcw_0_radar_rx0_0, 0), (self.blocks_null_sink_radar_rx_0, 0))
        self.connect((self.lora_sdr_fmcw_0_radar_rx0_0, 0), (self.blocks_tag_debug_2, 0))
        self.connect((self.lora_sdr_gray_demap_0_0, 0), (self.lora_sdr_fmcw_0_modulate0_0, 0))
        self.connect((self.lora_sdr_gray_mapping_0, 0), (self.lora_sdr_deinterleaver_0, 0))
        self.connect((self.lora_sdr_hamming_dec_0, 0), (self.lora_sdr_header_decoder_0, 0))
        self.connect((self.lora_sdr_hamming_enc_0_0, 0), (self.lora_sdr_interleaver_0_0, 0))
        self.connect((self.lora_sdr_header_0_0, 0), (self.lora_sdr_add_crc_0_0, 0))
        self.connect((self.lora_sdr_header_decoder_0, 0), (self.lora_sdr_dewhitening_0, 0))
        self.connect((self.lora_sdr_interleaver_0_0, 0), (self.lora_sdr_gray_demap_0_0, 0))
        self.connect((self.lora_sdr_whitening_0_0, 0), (self.lora_sdr_header_0_0, 0))
        self.connect((self.radar_signal_generator_fmcw_c_0, 0), (self.blocks_tag_debug_1, 0))
        self.connect((self.radar_signal_generator_fmcw_c_0, 0), (self.blocks_tagged_stream_mux_0, 0))
        self.connect((self.radar_signal_generator_fmcw_c_1, 0), (self.blocks_multiply_conjugate_cc_0, 0))
        self.connect((self.radar_signal_generator_fmcw_c_1, 0), (self.radar_static_target_simulator_cc_0, 0))
        self.connect((self.radar_split_cc_0, 0), (self.radar_ts_fft_cc_0, 0))
        self.connect((self.radar_split_cc_0_0, 0), (self.radar_ts_fft_cc_0_0, 0))
        self.connect((self.radar_static_target_simulator_cc_0, 0), (self.blocks_multiply_conjugate_cc_0, 1))
        self.connect((self.radar_static_target_simulator_cc_0, 0), (self.lora_sdr_fmcw_0_radar_rx0_0, 0))
        self.connect((self.radar_ts_fft_cc_0, 0), (self.radar_find_max_peak_c_0, 0))
        self.connect((self.radar_ts_fft_cc_0_0, 0), (self.radar_find_max_peak_c_0_0, 0))


    def get_sf(self):
        return self.sf

    def set_sf(self, sf):
        self.sf = sf
        self.set_channel_startup_guard(self.preamb_len * 2 * int((2**self.sf) * self.samp_rate / self.bw))
        self.set_radar_half_chirp_samples(int((2**self.sf) * self.samp_rate / self.bw))
        self.set_radar_rx_capture_samples(self.preamb_len * 2 * int((2**self.sf) * self.samp_rate / self.bw))
        self.lora_sdr_gray_demap_0_0.set_sf(self.sf)
        self.lora_sdr_hamming_enc_0_0.set_sf(self.sf)
        self.lora_sdr_interleaver_0_0.set_sf(self.sf)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_os_factor(int(self.samp_rate / self.bw))
        self.set_channel_startup_guard(self.preamb_len * 2 * int((2**self.sf) * self.samp_rate / self.bw))
        self.set_radar_half_chirp_samples(int((2**self.sf) * self.samp_rate / self.bw))
        self.set_radar_rx_capture_samples(self.preamb_len * 2 * int((2**self.sf) * self.samp_rate / self.bw))
        self.blocks_throttle2_0.set_sample_rate(self.samp_rate)
        self.channels_channel_model_0.set_frequency_offset((self.center_freq*self.clk_offset*1e-6/self.samp_rate))
        self.radar_static_target_simulator_cc_0.setup_targets([self.radar_target_range], [self.radar_target_velocity], [self.radar_target_rcs], [0], [0], self.samp_rate, self.center_freq, -10, True, self.radar_self_coupling)

    def get_preamb_len(self):
        return self.preamb_len

    def set_preamb_len(self, preamb_len):
        self.preamb_len = preamb_len
        self.set_channel_startup_guard(self.preamb_len * 2 * int((2**self.sf) * self.samp_rate / self.bw))
        self.set_radar_rx_capture_samples(self.preamb_len * 2 * int((2**self.sf) * self.samp_rate / self.bw))

    def get_capture_out_dir(self):
        return self.capture_out_dir

    def set_capture_out_dir(self, capture_out_dir):
        self.capture_out_dir = capture_out_dir
        self.set_radar_rx_capture_path(self.capture_out_dir + "/lora_fmcw_0_test1_radar_rx.dat")

    def get_bw(self):
        return self.bw

    def set_bw(self, bw):
        self.bw = bw
        self.set_os_factor(int(self.samp_rate / self.bw))
        self.set_channel_startup_guard(self.preamb_len * 2 * int((2**self.sf) * self.samp_rate / self.bw))
        self.set_fmcw_freq_cw(-0.45 * self.bw)
        self.set_fmcw_freq_sweep(0.90 * self.bw)
        self.set_radar_half_chirp_samples(int((2**self.sf) * self.samp_rate / self.bw))
        self.set_radar_rx_capture_samples(self.preamb_len * 2 * int((2**self.sf) * self.samp_rate / self.bw))

    def get_sync_word(self):
        return self.sync_word

    def set_sync_word(self, sync_word):
        self.sync_word = sync_word

    def get_soft_decoding(self):
        return self.soft_decoding

    def set_soft_decoding(self, soft_decoding):
        self.soft_decoding = soft_decoding

    def get_radar_target_velocity(self):
        return self.radar_target_velocity

    def set_radar_target_velocity(self, radar_target_velocity):
        self.radar_target_velocity = radar_target_velocity
        self.radar_static_target_simulator_cc_0.setup_targets([self.radar_target_range], [self.radar_target_velocity], [self.radar_target_rcs], [0], [0], self.samp_rate, self.center_freq, -10, True, self.radar_self_coupling)

    def get_radar_target_rcs(self):
        return self.radar_target_rcs

    def set_radar_target_rcs(self, radar_target_rcs):
        self.radar_target_rcs = radar_target_rcs
        self.radar_static_target_simulator_cc_0.setup_targets([self.radar_target_range], [self.radar_target_velocity], [self.radar_target_rcs], [0], [0], self.samp_rate, self.center_freq, -10, True, self.radar_self_coupling)

    def get_radar_target_range(self):
        return self.radar_target_range

    def set_radar_target_range(self, radar_target_range):
        self.radar_target_range = radar_target_range
        self.radar_static_target_simulator_cc_0.setup_targets([self.radar_target_range], [self.radar_target_velocity], [self.radar_target_rcs], [0], [0], self.samp_rate, self.center_freq, -10, True, self.radar_self_coupling)

    def get_radar_self_coupling(self):
        return self.radar_self_coupling

    def set_radar_self_coupling(self, radar_self_coupling):
        self.radar_self_coupling = radar_self_coupling
        self.radar_static_target_simulator_cc_0.setup_targets([self.radar_target_range], [self.radar_target_velocity], [self.radar_target_rcs], [0], [0], self.samp_rate, self.center_freq, -10, True, self.radar_self_coupling)

    def get_radar_rx_capture_samples(self):
        return self.radar_rx_capture_samples

    def set_radar_rx_capture_samples(self, radar_rx_capture_samples):
        self.radar_rx_capture_samples = radar_rx_capture_samples
        self.blocks_head_radar_rx_capture_0.set_length(self.radar_rx_capture_samples)

    def get_radar_rx_capture_path(self):
        return self.radar_rx_capture_path

    def set_radar_rx_capture_path(self, radar_rx_capture_path):
        self.radar_rx_capture_path = radar_rx_capture_path
        self.blocks_file_sink_radar_rx_capture_0.open(self.radar_rx_capture_path)

    def get_radar_peak_threshold(self):
        return self.radar_peak_threshold

    def set_radar_peak_threshold(self, radar_peak_threshold):
        self.radar_peak_threshold = radar_peak_threshold
        self.radar_find_max_peak_c_0.set_threshold(self.radar_peak_threshold)
        self.radar_find_max_peak_c_0_0.set_threshold(self.radar_peak_threshold)

    def get_radar_peak_protect(self):
        return self.radar_peak_protect

    def set_radar_peak_protect(self, radar_peak_protect):
        self.radar_peak_protect = radar_peak_protect
        self.radar_find_max_peak_c_0.set_samp_protect(self.radar_peak_protect)
        self.radar_find_max_peak_c_0_0.set_samp_protect(self.radar_peak_protect)

    def get_radar_half_chirp_samples(self):
        return self.radar_half_chirp_samples

    def set_radar_half_chirp_samples(self, radar_half_chirp_samples):
        self.radar_half_chirp_samples = radar_half_chirp_samples

    def get_radar_corr_threshold(self):
        return self.radar_corr_threshold

    def set_radar_corr_threshold(self, radar_corr_threshold):
        self.radar_corr_threshold = radar_corr_threshold

    def get_pay_len(self):
        return self.pay_len

    def set_pay_len(self, pay_len):
        self.pay_len = pay_len

    def get_os_factor(self):
        return self.os_factor

    def set_os_factor(self, os_factor):
        self.os_factor = os_factor

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

    def get_clk_offset(self):
        return self.clk_offset

    def set_clk_offset(self, clk_offset):
        self.clk_offset = clk_offset
        self.channels_channel_model_0.set_frequency_offset((self.center_freq*self.clk_offset*1e-6/self.samp_rate))
        self.channels_channel_model_0.set_timing_offset((1.0+self.clk_offset*1e-6))

    def get_channel_startup_guard(self):
        return self.channel_startup_guard

    def set_channel_startup_guard(self, channel_startup_guard):
        self.channel_startup_guard = channel_startup_guard
        self.blocks_delay_0.set_dly(int(self.channel_startup_guard))

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.channels_channel_model_0.set_frequency_offset((self.center_freq*self.clk_offset*1e-6/self.samp_rate))
        self.radar_static_target_simulator_cc_0.setup_targets([self.radar_target_range], [self.radar_target_velocity], [self.radar_target_rcs], [0], [0], self.samp_rate, self.center_freq, -10, True, self.radar_self_coupling)

    def get_SNRdB(self):
        return self.SNRdB

    def set_SNRdB(self, SNRdB):
        self.SNRdB = SNRdB
        self.channels_channel_model_0.set_noise_voltage((10**(-self.SNRdB/20)))




def main(top_block_cls=lora_fmcw_0_test1, options=None):
    tb = top_block_cls()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()
    tb.flowgraph_started.set()

    try:
        input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
