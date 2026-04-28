#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: LoRa FMCW Observe TF
# Description: Time-frequency observation flowgraph for radar/mod/mux/rx
# GNU Radio version: 3.10.11.0

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio import blocks
import pmt
from gnuradio import channels
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import radar
import gnuradio.lora_sdr_fmcw_0 as lora_sdr
import sip
import threading



class lora_fmcw_0_observe_tf(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "LoRa FMCW Observe TF", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("LoRa FMCW Observe TF")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("gnuradio/flowgraphs", "lora_fmcw_0_observe_tf")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)
        self.flowgraph_started = threading.Event()

        ##################################################
        # Variables
        ##################################################
        self.bw = bw = 125000
        self.sf = sf = 7
        self.samp_rate = samp_rate = bw*4
        self.preamb_len = preamb_len = 8
        self.sync_word = sync_word = 0x12
        self.soft_decoding = soft_decoding = False
        self.pay_len = pay_len = 255
        self.min_out_buffer = min_out_buffer = 65536
        self.max_out_buffer = max_out_buffer = 65536
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
        self.clk_offset = clk_offset = 0
        self.channel_startup_guard = channel_startup_guard = preamb_len * 2 * int((2**sf) * samp_rate / bw)
        self.center_freq = center_freq = 5800e6
        self.SNRdB = SNRdB = -7

        ##################################################
        # Blocks
        ##################################################

        self.radar_signal_generator_fmcw_c_0 = radar.signal_generator_fmcw_c(samp_rate, fmcw_up_len, fmcw_down_len, fmcw_cw_len, fmcw_freq_cw, fmcw_freq_sweep, 1, preamb_len, "frame_len", sf, bw)
        self.radar_signal_generator_fmcw_c_0.set_min_output_buffer(min_out_buffer)
        self.qtgui_waterfall_sink_x_rx = qtgui.waterfall_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            'RX input after channel', #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_waterfall_sink_x_rx.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_rx.enable_grid(False)
        self.qtgui_waterfall_sink_x_rx.enable_axis_labels(True)

        self.qtgui_waterfall_sink_x_rx.disable_legend()


        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_rx.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_rx.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_rx.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_rx.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_rx.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_rx_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_rx.qwidget(), Qt.QWidget)

        self.top_grid_layout.addWidget(self._qtgui_waterfall_sink_x_rx_win, 1, 1, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_waterfall_sink_x_radar_rx = qtgui.waterfall_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            'Radar RX accepted', #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_waterfall_sink_x_radar_rx.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_radar_rx.enable_grid(False)
        self.qtgui_waterfall_sink_x_radar_rx.enable_axis_labels(True)

        self.qtgui_waterfall_sink_x_radar_rx.disable_legend()


        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_radar_rx.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_radar_rx.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_radar_rx.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_radar_rx.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_radar_rx.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_radar_rx_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_radar_rx.qwidget(), Qt.QWidget)

        self.top_grid_layout.addWidget(self._qtgui_waterfall_sink_x_radar_rx_win, 2, 0, 1, 2)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_waterfall_sink_x_radar = qtgui.waterfall_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            'Radar output', #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_waterfall_sink_x_radar.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_radar.enable_grid(False)
        self.qtgui_waterfall_sink_x_radar.enable_axis_labels(True)

        self.qtgui_waterfall_sink_x_radar.disable_legend()


        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_radar.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_radar.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_radar.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_radar.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_radar.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_radar_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_radar.qwidget(), Qt.QWidget)

        self.top_grid_layout.addWidget(self._qtgui_waterfall_sink_x_radar_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_waterfall_sink_x_mux = qtgui.waterfall_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            'True MUX output', #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_waterfall_sink_x_mux.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_mux.enable_grid(False)
        self.qtgui_waterfall_sink_x_mux.enable_axis_labels(True)

        self.qtgui_waterfall_sink_x_mux.disable_legend()


        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_mux.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_mux.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_mux.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_mux.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_mux.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_mux_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_mux.qwidget(), Qt.QWidget)

        self.top_grid_layout.addWidget(self._qtgui_waterfall_sink_x_mux_win, 1, 0, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_waterfall_sink_x_mod = qtgui.waterfall_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            'Modulate0 output', #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_waterfall_sink_x_mod.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_mod.enable_grid(False)
        self.qtgui_waterfall_sink_x_mod.enable_axis_labels(True)

        self.qtgui_waterfall_sink_x_mod.disable_legend()


        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_mod.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_mod.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_mod.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_mod.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_mod.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_mod_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_mod.qwidget(), Qt.QWidget)

        self.top_grid_layout.addWidget(self._qtgui_waterfall_sink_x_mod_win, 0, 1, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.lora_sdr_whitening_0_0 = lora_sdr.whitening(True,True,',','packet_len')
        self.lora_sdr_payload_id_inc_0 = lora_sdr.payload_id_inc(':')
        self.lora_sdr_interleaver_0_0 = lora_sdr.interleaver(cr, sf, 0, bw)
        self.lora_sdr_header_decoder_0 = lora_sdr.header_decoder(impl_head, cr, pay_len, has_crc, 2, True)
        self.lora_sdr_header_0_0 = lora_sdr.header(impl_head, has_crc, cr)
        self.lora_sdr_hamming_enc_0_0 = lora_sdr.hamming_enc(cr, sf)
        self.lora_sdr_hamming_dec_0 = lora_sdr.hamming_dec(soft_decoding)
        self.lora_sdr_gray_mapping_0 = lora_sdr.gray_mapping( soft_decoding)
        self.lora_sdr_gray_demap_0_0 = lora_sdr.gray_demap(sf)
        self.lora_sdr_fmcw_0_modulate0_0 = lora_sdr.modulate0(sf, samp_rate, bw, [sync_word], 4096,preamb_len)
        self.lora_sdr_fmcw_0_modulate0_0.set_min_output_buffer(min_out_buffer)
        self.lora_sdr_fmcw_0_frame_sync0_0 = lora_sdr.frame_sync0(center_freq, bw, sf, impl_head, [sync_word], 4,preamb_len, corr_threshold)
        self.lora_sdr_fmcw_0_radar_rx0_0 = lora_sdr.radar_rx0(bw, sf, 4, corr_threshold, "radar_len")
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
        self.blocks_tagged_stream_mux_0 = blocks.tagged_stream_mux(gr.sizeof_gr_complex*1, 'frame_len', 0)
        self.blocks_tagged_stream_mux_0.set_min_output_buffer(2097152)
        self.blocks_message_strobe_0_0_0 = blocks.message_strobe(pmt.intern("ASDFGHJKLZXCVB : 0"), frame_period)
        self.blocks_delay_0 = blocks.delay(gr.sizeof_gr_complex*1, channel_startup_guard)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_message_strobe_0_0_0, 'strobe'), (self.lora_sdr_payload_id_inc_0, 'msg_in'))
        self.msg_connect((self.blocks_message_strobe_0_0_0, 'strobe'), (self.lora_sdr_whitening_0_0, 'msg'))
        self.msg_connect((self.lora_sdr_header_decoder_0, 'frame_info'), (self.lora_sdr_fmcw_0_frame_sync0_0, 'frame_info'))
        self.msg_connect((self.lora_sdr_payload_id_inc_0, 'msg_out'), (self.blocks_message_strobe_0_0_0, 'set_msg'))
        self.connect((self.blocks_delay_0, 0), (self.channels_channel_model_0, 0))
        self.connect((self.blocks_tagged_stream_mux_0, 0), (self.blocks_throttle2_0, 0))
        self.connect((self.blocks_tagged_stream_mux_0, 0), (self.qtgui_waterfall_sink_x_mux, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.blocks_delay_0, 0))
        self.connect((self.channels_channel_model_0, 0), (self.lora_sdr_fmcw_0_frame_sync0_0, 0))
        self.connect((self.channels_channel_model_0, 0), (self.lora_sdr_fmcw_0_radar_rx0_0, 0))
        self.connect((self.channels_channel_model_0, 0), (self.qtgui_waterfall_sink_x_rx, 0))
        self.connect((self.lora_sdr_add_crc_0_0, 0), (self.lora_sdr_hamming_enc_0_0, 0))
        self.connect((self.lora_sdr_deinterleaver_0, 0), (self.lora_sdr_hamming_dec_0, 0))
        self.connect((self.lora_sdr_dewhitening_0, 0), (self.lora_sdr_crc_verif_0, 0))
        self.connect((self.lora_sdr_fft_demod_0, 0), (self.lora_sdr_gray_mapping_0, 0))
        self.connect((self.lora_sdr_fmcw_0_frame_sync0_0, 0), (self.lora_sdr_fft_demod_0, 0))
        self.connect((self.lora_sdr_fmcw_0_modulate0_0, 0), (self.blocks_tagged_stream_mux_0, 1))
        self.connect((self.lora_sdr_fmcw_0_modulate0_0, 0), (self.qtgui_waterfall_sink_x_mod, 0))
        self.connect((self.lora_sdr_fmcw_0_radar_rx0_0, 0), (self.qtgui_waterfall_sink_x_radar_rx, 0))
        self.connect((self.lora_sdr_gray_demap_0_0, 0), (self.lora_sdr_fmcw_0_modulate0_0, 0))
        self.connect((self.lora_sdr_gray_mapping_0, 0), (self.lora_sdr_deinterleaver_0, 0))
        self.connect((self.lora_sdr_hamming_dec_0, 0), (self.lora_sdr_header_decoder_0, 0))
        self.connect((self.lora_sdr_hamming_enc_0_0, 0), (self.lora_sdr_interleaver_0_0, 0))
        self.connect((self.lora_sdr_header_0_0, 0), (self.lora_sdr_add_crc_0_0, 0))
        self.connect((self.lora_sdr_header_decoder_0, 0), (self.lora_sdr_dewhitening_0, 0))
        self.connect((self.lora_sdr_interleaver_0_0, 0), (self.lora_sdr_gray_demap_0_0, 0))
        self.connect((self.lora_sdr_whitening_0_0, 0), (self.lora_sdr_header_0_0, 0))
        self.connect((self.radar_signal_generator_fmcw_c_0, 0), (self.blocks_tagged_stream_mux_0, 0))
        self.connect((self.radar_signal_generator_fmcw_c_0, 0), (self.qtgui_waterfall_sink_x_radar, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("gnuradio/flowgraphs", "lora_fmcw_0_observe_tf")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_bw(self):
        return self.bw

    def set_bw(self, bw):
        self.bw = bw
        self.set_channel_startup_guard(self.preamb_len * 2 * int((2**self.sf) * self.samp_rate / self.bw))
        self.set_fmcw_freq_cw(-0.45 * self.bw)
        self.set_fmcw_freq_sweep(0.90 * self.bw)
        self.set_samp_rate(self.bw*4)

    def get_sf(self):
        return self.sf

    def set_sf(self, sf):
        self.sf = sf
        self.set_channel_startup_guard(self.preamb_len * 2 * int((2**self.sf) * self.samp_rate / self.bw))
        self.lora_sdr_gray_demap_0_0.set_sf(self.sf)
        self.lora_sdr_hamming_enc_0_0.set_sf(self.sf)
        self.lora_sdr_interleaver_0_0.set_sf(self.sf)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_channel_startup_guard(self.preamb_len * 2 * int((2**self.sf) * self.samp_rate / self.bw))
        self.blocks_throttle2_0.set_sample_rate(self.samp_rate)
        self.channels_channel_model_0.set_frequency_offset((self.center_freq*self.clk_offset*1e-6/self.samp_rate))
        self.qtgui_waterfall_sink_x_radar.set_frequency_range(0, self.samp_rate)
        self.qtgui_waterfall_sink_x_mod.set_frequency_range(0, self.samp_rate)
        self.qtgui_waterfall_sink_x_mux.set_frequency_range(0, self.samp_rate)
        self.qtgui_waterfall_sink_x_rx.set_frequency_range(0, self.samp_rate)
        self.qtgui_waterfall_sink_x_radar_rx.set_frequency_range(0, self.samp_rate)

    def get_preamb_len(self):
        return self.preamb_len

    def set_preamb_len(self, preamb_len):
        self.preamb_len = preamb_len
        self.set_channel_startup_guard(self.preamb_len * 2 * int((2**self.sf) * self.samp_rate / self.bw))

    def get_sync_word(self):
        return self.sync_word

    def set_sync_word(self, sync_word):
        self.sync_word = sync_word

    def get_soft_decoding(self):
        return self.soft_decoding

    def set_soft_decoding(self, soft_decoding):
        self.soft_decoding = soft_decoding

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
        self.lora_sdr_fmcw_0_radar_rx0_0.set_corr_threshold(self.corr_threshold)

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

    def get_SNRdB(self):
        return self.SNRdB

    def set_SNRdB(self, SNRdB):
        self.SNRdB = SNRdB
        self.channels_channel_model_0.set_noise_voltage((10**(-self.SNRdB/20)))




def main(top_block_cls=lora_fmcw_0_observe_tf, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()
    tb.flowgraph_started.set()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
