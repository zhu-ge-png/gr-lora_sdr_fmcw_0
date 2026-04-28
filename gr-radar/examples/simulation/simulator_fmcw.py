#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Simulator Fmcw
# GNU Radio version: 3.10.11.0

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from gnuradio import analog
from gnuradio import blocks
from gnuradio import filter
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
import sip
import threading



class simulator_fmcw(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Simulator Fmcw", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Simulator Fmcw")
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

        self.settings = Qt.QSettings("gnuradio/flowgraphs", "simulator_fmcw")

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
        self.samp_up = samp_up = 2**14
        self.sweep_freq = sweep_freq = 6e6
        self.samp_rate = samp_rate = 10000000
        self.samp_down = samp_down = samp_up
        self.samp_cw = samp_cw = 2**14
        self.center_freq = center_freq = 5.9e9
        self.velocity = velocity = 0
        self.value_range = value_range = 200
        self.v_res = v_res = samp_rate/samp_cw*3e8/2/center_freq
        self.threshold = threshold = -120
        self.range_res = range_res = 3e8/2/sweep_freq
        self.protect_samp = protect_samp = 1
        self.min_out_buffer = min_out_buffer = int((samp_up+samp_down+samp_cw)*2)
        self.meas_duration = meas_duration = (samp_cw+samp_up+samp_down)/float(samp_rate)
        self.max_out_buffer = max_out_buffer = 0
        self.decim_fac = decim_fac = 2**5

        ##################################################
        # Blocks
        ##################################################

        self._velocity_range = qtgui.Range(0, 100, 1, 0, 200)
        self._velocity_win = qtgui.RangeWidget(self._velocity_range, self.set_velocity, "'velocity'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._velocity_win)
        self._value_range_range = qtgui.Range(0, 1000, 1, 200, 200)
        self._value_range_win = qtgui.RangeWidget(self._value_range_range, self.set_value_range, "range", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._value_range_win)
        self._threshold_range = qtgui.Range(-120, 0, 1, -120, 200)
        self._threshold_win = qtgui.RangeWidget(self._threshold_range, self.set_threshold, "'threshold'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._threshold_win)
        self._protect_samp_range = qtgui.Range(0, 100, 1, 1, 200)
        self._protect_samp_win = qtgui.RangeWidget(self._protect_samp_range, self.set_protect_samp, "'protect_samp'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._protect_samp_win)
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=1,
                decimation=decim_fac,
                taps=[],
                fractional_bw=0)
        self.radar_ts_fft_cc_0_1 = radar.ts_fft_cc((samp_down//decim_fac),  "packet_len")
        self.radar_ts_fft_cc_0_0 = radar.ts_fft_cc((samp_up//decim_fac),  "packet_len")
        self.radar_ts_fft_cc_0 = radar.ts_fft_cc((samp_cw//decim_fac),  "packet_len")
        self.radar_static_target_simulator_cc_0 = radar.static_target_simulator_cc([value_range], [velocity], [1e16], [0], [0], samp_rate, center_freq, -10, True, True, "packet_len")
        self.radar_static_target_simulator_cc_0.set_min_output_buffer(min_out_buffer)
        self.radar_split_cc_0_0_0 = radar.split_cc(2, [samp_cw//decim_fac,samp_up//decim_fac,samp_down//decim_fac], "packet_len")
        self.radar_split_cc_0_0_0.set_min_output_buffer(min_out_buffer)
        self.radar_split_cc_0_0 = radar.split_cc(1, [samp_cw//decim_fac,samp_up//decim_fac,samp_down//decim_fac], "packet_len")
        self.radar_split_cc_0_0.set_min_output_buffer(min_out_buffer)
        self.radar_split_cc_0 = radar.split_cc(0, [samp_cw//decim_fac,samp_up//decim_fac,samp_down//decim_fac], "packet_len")
        self.radar_split_cc_0.set_min_output_buffer(min_out_buffer)
        self.radar_signal_generator_fmcw_c_0 = radar.signal_generator_fmcw_c(samp_rate, samp_up, samp_down, samp_cw, -sweep_freq/2, sweep_freq, 1, 1, "packet_len", 0, 0.0)
        self.radar_signal_generator_fmcw_c_0.set_min_output_buffer(min_out_buffer)
        self.radar_print_results_0 = radar.print_results(False, "")
        self.radar_find_max_peak_c_0_0_0 = radar.find_max_peak_c((samp_rate//decim_fac), threshold, protect_samp, [1,1], False, "packet_len")
        self.radar_find_max_peak_c_0_0 = radar.find_max_peak_c((samp_rate//decim_fac), threshold, protect_samp, [1,1], False, "packet_len")
        self.radar_find_max_peak_c_0 = radar.find_max_peak_c((samp_rate//decim_fac), threshold, protect_samp, [1,1], False, "packet_len")
        self.radar_estimator_fmcw_0 = radar.estimator_fmcw((samp_rate//decim_fac), center_freq, sweep_freq, (samp_up//decim_fac), (samp_down//decim_fac), False)
        self.qtgui_sink_x_0_0_0 = qtgui.sink_c(
            (samp_up//decim_fac), #fftsize
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            (samp_rate/decim_fac), #bw
            'DOWN', #name
            True, #plotfreq
            True, #plotwaterfall
            True, #plottime
            True, #plotconst
            None # parent
        )
        self.qtgui_sink_x_0_0_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_0_0_win = sip.wrapinstance(self.qtgui_sink_x_0_0_0.qwidget(), Qt.QWidget)

        self.qtgui_sink_x_0_0_0.enable_rf_freq(False)

        self.top_layout.addWidget(self._qtgui_sink_x_0_0_0_win)
        self.qtgui_sink_x_0_0 = qtgui.sink_c(
            (samp_up//decim_fac), #fftsize
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            (samp_rate/decim_fac), #bw
            'UP', #name
            True, #plotfreq
            True, #plotwaterfall
            True, #plottime
            True, #plotconst
            None # parent
        )
        self.qtgui_sink_x_0_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_0_win = sip.wrapinstance(self.qtgui_sink_x_0_0.qwidget(), Qt.QWidget)

        self.qtgui_sink_x_0_0.enable_rf_freq(False)

        self.top_layout.addWidget(self._qtgui_sink_x_0_0_win)
        self.qtgui_sink_x_0 = qtgui.sink_c(
            (samp_cw//decim_fac), #fftsize
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            (samp_rate/decim_fac), #bw
            'CW', #name
            False, #plotfreq
            True, #plotwaterfall
            True, #plottime
            True, #plotconst
            None # parent
        )
        self.qtgui_sink_x_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_win = sip.wrapinstance(self.qtgui_sink_x_0.qwidget(), Qt.QWidget)

        self.qtgui_sink_x_0.enable_rf_freq(False)

        self.top_layout.addWidget(self._qtgui_sink_x_0_win)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_throttle_0.set_min_output_buffer(min_out_buffer)
        self.blocks_tagged_stream_multiply_length_0 = blocks.tagged_stream_multiply_length(gr.sizeof_gr_complex*1, "packet_len", (1.0/decim_fac))
        self.blocks_tagged_stream_multiply_length_0.set_min_output_buffer(min_out_buffer)
        self.blocks_multiply_conjugate_cc_0 = blocks.multiply_conjugate_cc(1)
        self.blocks_multiply_conjugate_cc_0.set_min_output_buffer(min_out_buffer)
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        self.blocks_add_xx_0.set_min_output_buffer(min_out_buffer)
        self.analog_noise_source_x_0 = analog.noise_source_c(analog.GR_GAUSSIAN, 0.1, 0)
        self.analog_noise_source_x_0.set_min_output_buffer(min_out_buffer)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.radar_estimator_fmcw_0, 'Msg out'), (self.radar_print_results_0, 'Msg in'))
        self.msg_connect((self.radar_find_max_peak_c_0, 'Msg out'), (self.radar_estimator_fmcw_0, 'Msg in CW'))
        self.msg_connect((self.radar_find_max_peak_c_0_0, 'Msg out'), (self.radar_estimator_fmcw_0, 'Msg in UP'))
        self.msg_connect((self.radar_find_max_peak_c_0_0_0, 'Msg out'), (self.radar_estimator_fmcw_0, 'Msg in DOWN'))
        self.connect((self.analog_noise_source_x_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_multiply_conjugate_cc_0, 1))
        self.connect((self.blocks_multiply_conjugate_cc_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.blocks_tagged_stream_multiply_length_0, 0), (self.radar_split_cc_0, 0))
        self.connect((self.blocks_tagged_stream_multiply_length_0, 0), (self.radar_split_cc_0_0, 0))
        self.connect((self.blocks_tagged_stream_multiply_length_0, 0), (self.radar_split_cc_0_0_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.radar_static_target_simulator_cc_0, 0))
        self.connect((self.radar_signal_generator_fmcw_c_0, 0), (self.blocks_multiply_conjugate_cc_0, 0))
        self.connect((self.radar_signal_generator_fmcw_c_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.radar_split_cc_0, 0), (self.qtgui_sink_x_0, 0))
        self.connect((self.radar_split_cc_0, 0), (self.radar_ts_fft_cc_0, 0))
        self.connect((self.radar_split_cc_0_0, 0), (self.qtgui_sink_x_0_0, 0))
        self.connect((self.radar_split_cc_0_0, 0), (self.radar_ts_fft_cc_0_0, 0))
        self.connect((self.radar_split_cc_0_0_0, 0), (self.qtgui_sink_x_0_0_0, 0))
        self.connect((self.radar_split_cc_0_0_0, 0), (self.radar_ts_fft_cc_0_1, 0))
        self.connect((self.radar_static_target_simulator_cc_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.radar_ts_fft_cc_0, 0), (self.radar_find_max_peak_c_0, 0))
        self.connect((self.radar_ts_fft_cc_0_0, 0), (self.radar_find_max_peak_c_0_0, 0))
        self.connect((self.radar_ts_fft_cc_0_1, 0), (self.radar_find_max_peak_c_0_0_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.blocks_tagged_stream_multiply_length_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("gnuradio/flowgraphs", "simulator_fmcw")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_up(self):
        return self.samp_up

    def set_samp_up(self, samp_up):
        self.samp_up = samp_up
        self.set_meas_duration((self.samp_cw+self.samp_up+self.samp_down)/float(self.samp_rate))
        self.set_min_out_buffer(int((self.samp_up+self.samp_down+self.samp_cw)*2))
        self.set_samp_down(self.samp_up)

    def get_sweep_freq(self):
        return self.sweep_freq

    def set_sweep_freq(self, sweep_freq):
        self.sweep_freq = sweep_freq
        self.set_range_res(3e8/2/self.sweep_freq)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_meas_duration((self.samp_cw+self.samp_up+self.samp_down)/float(self.samp_rate))
        self.set_v_res(self.samp_rate/self.samp_cw*3e8/2/self.center_freq)
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)
        self.qtgui_sink_x_0.set_frequency_range(0, (self.samp_rate/self.decim_fac))
        self.qtgui_sink_x_0_0.set_frequency_range(0, (self.samp_rate/self.decim_fac))
        self.qtgui_sink_x_0_0_0.set_frequency_range(0, (self.samp_rate/self.decim_fac))
        self.radar_static_target_simulator_cc_0.setup_targets([self.value_range], [self.velocity], [1e16], [0], [0], self.samp_rate, self.center_freq, -10, True, True)

    def get_samp_down(self):
        return self.samp_down

    def set_samp_down(self, samp_down):
        self.samp_down = samp_down
        self.set_meas_duration((self.samp_cw+self.samp_up+self.samp_down)/float(self.samp_rate))
        self.set_min_out_buffer(int((self.samp_up+self.samp_down+self.samp_cw)*2))

    def get_samp_cw(self):
        return self.samp_cw

    def set_samp_cw(self, samp_cw):
        self.samp_cw = samp_cw
        self.set_meas_duration((self.samp_cw+self.samp_up+self.samp_down)/float(self.samp_rate))
        self.set_min_out_buffer(int((self.samp_up+self.samp_down+self.samp_cw)*2))
        self.set_v_res(self.samp_rate/self.samp_cw*3e8/2/self.center_freq)

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.set_v_res(self.samp_rate/self.samp_cw*3e8/2/self.center_freq)
        self.radar_static_target_simulator_cc_0.setup_targets([self.value_range], [self.velocity], [1e16], [0], [0], self.samp_rate, self.center_freq, -10, True, True)

    def get_velocity(self):
        return self.velocity

    def set_velocity(self, velocity):
        self.velocity = velocity
        self.radar_static_target_simulator_cc_0.setup_targets([self.value_range], [self.velocity], [1e16], [0], [0], self.samp_rate, self.center_freq, -10, True, True)

    def get_value_range(self):
        return self.value_range

    def set_value_range(self, value_range):
        self.value_range = value_range
        self.radar_static_target_simulator_cc_0.setup_targets([self.value_range], [self.velocity], [1e16], [0], [0], self.samp_rate, self.center_freq, -10, True, True)

    def get_v_res(self):
        return self.v_res

    def set_v_res(self, v_res):
        self.v_res = v_res

    def get_threshold(self):
        return self.threshold

    def set_threshold(self, threshold):
        self.threshold = threshold
        self.radar_find_max_peak_c_0.set_threshold(self.threshold)
        self.radar_find_max_peak_c_0_0.set_threshold(self.threshold)
        self.radar_find_max_peak_c_0_0_0.set_threshold(self.threshold)

    def get_range_res(self):
        return self.range_res

    def set_range_res(self, range_res):
        self.range_res = range_res

    def get_protect_samp(self):
        return self.protect_samp

    def set_protect_samp(self, protect_samp):
        self.protect_samp = protect_samp
        self.radar_find_max_peak_c_0.set_samp_protect(self.protect_samp)
        self.radar_find_max_peak_c_0_0.set_samp_protect(self.protect_samp)
        self.radar_find_max_peak_c_0_0_0.set_samp_protect(self.protect_samp)

    def get_min_out_buffer(self):
        return self.min_out_buffer

    def set_min_out_buffer(self, min_out_buffer):
        self.min_out_buffer = min_out_buffer

    def get_meas_duration(self):
        return self.meas_duration

    def set_meas_duration(self, meas_duration):
        self.meas_duration = meas_duration

    def get_max_out_buffer(self):
        return self.max_out_buffer

    def set_max_out_buffer(self, max_out_buffer):
        self.max_out_buffer = max_out_buffer

    def get_decim_fac(self):
        return self.decim_fac

    def set_decim_fac(self, decim_fac):
        self.decim_fac = decim_fac
        self.blocks_tagged_stream_multiply_length_0.set_scalar((1.0/self.decim_fac))
        self.qtgui_sink_x_0.set_frequency_range(0, (self.samp_rate/self.decim_fac))
        self.qtgui_sink_x_0_0.set_frequency_range(0, (self.samp_rate/self.decim_fac))
        self.qtgui_sink_x_0_0_0.set_frequency_range(0, (self.samp_rate/self.decim_fac))




def main(top_block_cls=simulator_fmcw, options=None):

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
