#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Simulator Fmcw
# GNU Radio version: 3.10.9.2

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

# =====================
# 该脚本由 GRC 生成：FMCW 雷达仿真流程图
# 重点看 3 个部分：Variables(参数)、Blocks(模块)、Connections(连线/数据流)
# 核心信号链：FMCW产生 -> 目标回波模拟 -> 加噪 -> 去斜(乘共轭) -> 降采样/修正tag -> 分段(CW/UP/DOWN) -> FFT -> 找峰值
# packet_len 是“每一帧/一次测量”的 tag 名称，用来让 split/FFT/find_peak 按帧处理
# =====================




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

        self.settings = Qt.QSettings("GNU Radio", "simulator_fmcw")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        # Variables 里定义了 FMCW 的关键参数（下面这些变量会被各个 radar 块引用）：
        # - samp_rate: 采样率(Hz)
        # - sweep_freq: FMCW 线性调频带宽(Hz)
        # - samp_cw / samp_up / samp_down: CW段 / 上扫段 / 下扫段 的采样点数
        # - center_freq: 雷达载频(Hz)；用于多普勒/速度换算
        # - value_range: 目标距离(米)；通过 static_target_simulator_cc 生成相应时延
        # - velocity: 目标径向速度(米/秒)；通过 static_target_simulator_cc 生成多普勒
        # - range_res = c/(2*B): 距离分辨率（理想情况下 B=sweep_freq）
        # - v_res ≈ (PRF)*c/(2*fc): 速度分辨率（这里 PRF 由 CW 段长度决定：PRF≈samp_rate/samp_cw）
        # - decim_fac: 降采样因子（rational_resampler 用）；降采样后采样率变为 samp_rate/decim_fac
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
        # Blocks 里实例化了 GRC 里的每一个“方块”。下面在每个 block 创建语句前，我插入了中文注释：
        # - 输入/输出端口是什么
        # - 它在 FMCW 信号处理链中承担什么作用
        ##################################################

        # [GUI] 速度(velocity)滑块范围设置
        # - 输入：无（Qt 控件）
        # - 输出：用户拖动时触发回调 set_velocity(velocity)
        self._velocity_range = qtgui.Range(0, 100, 1, 0, 200)
        self._velocity_win = qtgui.RangeWidget(self._velocity_range, self.set_velocity, "'velocity'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._velocity_win)
        # [GUI] 距离(range/value_range)滑块范围设置
        # - 输出：用户拖动时触发回调 set_value_range(value_range)
        self._value_range_range = qtgui.Range(0, 1000, 1, 200, 200)
        self._value_range_win = qtgui.RangeWidget(self._value_range_range, self.set_value_range, "range", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._value_range_win)
        # [GUI] 峰值检测阈值(threshold)滑块
        # - 输出：触发 set_threshold(threshold)，用于 find_max_peak 块的门限
        self._threshold_range = qtgui.Range(-120, 0, 1, -120, 200)
        self._threshold_win = qtgui.RangeWidget(self._threshold_range, self.set_threshold, "'threshold'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._threshold_win)
        # [GUI] protect_samp 滑块（峰值保护区/忽略区长度）
        # - 输出：触发 set_protect_samp(protect_samp)，用于 find_max_peak 避免重复选峰
        self._protect_samp_range = qtgui.Range(0, 100, 1, 1, 200)
        self._protect_samp_win = qtgui.RangeWidget(self._protect_samp_range, self.set_protect_samp, "'protect_samp'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._protect_samp_win)
        # [DSP] rational_resampler_ccc（整数降采样）
        # - 输入：complex stream（去斜后的 beat 信号），带 packet_len tag
        # - 输出：complex stream（采样率降低为 samp_rate/decim_fac）
        # - 注意：降采样会让“每帧长度”也缩短，但 tag 仍然是旧长度，因此后面用 tagged_stream_multiply_length 修正 packet_len
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=1,
                decimation=decim_fac,
                taps=[],
                fractional_bw=0)
        # [Radar DSP] ts_fft_cc（按 tag 分帧做 FFT）——用于 DOWN 段
        # - 输入：DOWN 段的 complex time stream（每帧长度 = samp_down/decim_fac，通过 tag packet_len 分帧）
        # - 输出：complex spectrum stream（FFT 输出，供 find_max_peak 检测峰值）
        self.radar_ts_fft_cc_0_1 = radar.ts_fft_cc((samp_down//decim_fac),  "packet_len")
        # [Radar DSP] ts_fft_cc ——用于 UP 段
        # - 输入：UP 段 beat 信号（每帧长度 = samp_up/decim_fac）
        # - 输出：频域谱
        self.radar_ts_fft_cc_0_0 = radar.ts_fft_cc((samp_up//decim_fac),  "packet_len")
        # [Radar DSP] ts_fft_cc ——用于 CW 段
        # - 输入：CW 段 beat 信号（每帧长度 = samp_cw/decim_fac）
        # - 输出：频域谱
        self.radar_ts_fft_cc_0 = radar.ts_fft_cc((samp_cw//decim_fac),  "packet_len")
        # [Radar Channel/Scene] static_target_simulator_cc（目标回波仿真器）
        # - 输入：发射信号 Tx（complex stream，来自 FMCW 发生器）
        # - 输出：接收回波 Rx（complex stream）
        # - 内部大致做的事：
        #   1) 根据目标距离 value_range 施加传播时延（相当于把信号延迟若干采样点）
        #   2) 根据目标速度 velocity 施加多普勒频移（相位随时间线性旋转，fd = 2*v*fc/c）
        #   3) 根据 RCS/衰减参数缩放幅度
        # - 这里通过 setup_targets(...) 在运行时更新目标参数（见 set_velocity / set_value_range / set_center_freq / set_samp_rate）
        self.radar_static_target_simulator_cc_0 = radar.static_target_simulator_cc([value_range], [velocity], [1e16], [0], [0], samp_rate, center_freq, -10, True, True, "packet_len")
        self.radar_static_target_simulator_cc_0.set_min_output_buffer(min_out_buffer)
        # [Radar DSP] split_cc（按 packet_len 把一帧切成 CW/UP/DOWN 三段，并选其中一段输出）
        # - 这个实例选择 index=2（通常对应 DOWN 段）
        # - 输入：一整帧 beat 信号
        # - 输出：DOWN 段 beat 信号（长度 = samp_down/decim_fac）
        self.radar_split_cc_0_0_0 = radar.split_cc(2, [samp_cw//decim_fac,samp_up//decim_fac,samp_down//decim_fac], "packet_len")
        self.radar_split_cc_0_0_0.set_min_output_buffer(min_out_buffer)
        # [Radar DSP] split_cc ——选择 index=1（通常对应 UP 段）
        # - 输出：UP 段 beat 信号（长度 = samp_up/decim_fac）
        self.radar_split_cc_0_0 = radar.split_cc(1, [samp_cw//decim_fac,samp_up//decim_fac,samp_down//decim_fac], "packet_len")
        self.radar_split_cc_0_0.set_min_output_buffer(min_out_buffer)
        # [Radar DSP] split_cc ——选择 index=0（通常对应 CW 段）
        # - 输出：CW 段 beat 信号（长度 = samp_cw/decim_fac）
        self.radar_split_cc_0 = radar.split_cc(0, [samp_cw//decim_fac,samp_up//decim_fac,samp_down//decim_fac], "packet_len")
        self.radar_split_cc_0.set_min_output_buffer(min_out_buffer)
        # [Source] signal_generator_fmcw_c（FMCW 发射波形发生器）
        # - 输出：complex stream（连续发射的 FMCW 波形）
        # - 每一帧由 3 段拼接：CW -> 上扫 chirp -> 下扫 chirp
        # - 参数含义（看构造函数传参）：
        #   * samp_rate: 采样率
        #   * samp_up/samp_down/samp_cw: 三段各自长度（采样点数）
        #   * -sweep_freq/2: 起始频偏（基带等效，让扫频居中）
        #   * sweep_freq: 扫频带宽
        #   * 1: 幅度/增益（这里为 1）
        #   * "packet_len": 给每帧打 tag（tag value=一帧总长度），用于后续 split/FFT 按帧处理
        self.radar_signal_generator_fmcw_c_0 = radar.signal_generator_fmcw_c(samp_rate, samp_up, samp_down, samp_cw, -sweep_freq/2, sweep_freq, 1, "packet_len")
        self.radar_signal_generator_fmcw_c_0.set_min_output_buffer(min_out_buffer)
        # [Radar DSP/Sink] find_max_peak_c（找最大峰值）——用于 DOWN 段 FFT 输出
        # - 输入：complex spectrum（来自 ts_fft_cc）
        # - 输出：一般是“打印/打 tag/消息端口”等形式汇报峰值（该块通常是 sink，不再往后连接）
        # - threshold: 门限（由 GUI 滑块实时更新）
        # - protect_samp: 保护区长度，避免主峰附近重复检峰
        self.radar_find_max_peak_c_0_0_0 = radar.find_max_peak_c((samp_rate//decim_fac), threshold, protect_samp, [1,1], False, "packet_len")
        # [Radar DSP/Sink] find_max_peak_c ——用于 UP 段
        self.radar_find_max_peak_c_0_0 = radar.find_max_peak_c((samp_rate//decim_fac), threshold, protect_samp, [1,1], False, "packet_len")
        # [Radar DSP/Sink] find_max_peak_c ——用于 CW 段
        self.radar_find_max_peak_c_0 = radar.find_max_peak_c((samp_rate//decim_fac), threshold, protect_samp, [1,1], False, "packet_len")
        # [GUI] Qt GUI Sink（显示 DOWN 段 beat 信号）
        # - 输入：complex stream（DOWN 段）
        # - 显示：频谱/瀑布/时域/星座
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
        # [GUI] Qt GUI Sink（显示 UP 段 beat 信号）
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
        # [GUI] Qt GUI Sink（显示 CW 段 beat 信号）
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
        # [DSP] Throttle（节流）
        # - 输入：Tx complex stream
        # - 输出：同样的 stream
        # - 作用：纯仿真时限制流图速度，避免 CPU 100% 占用
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_throttle_0.set_min_output_buffer(min_out_buffer)
        # [DSP/Tag] tagged_stream_multiply_length（修正 packet_len）
        # - 输入：已降采样的 complex stream
        # - 输出：相同样本，但把 tag "packet_len" 的 value 乘以 scalar=1/decim_fac
        self.blocks_tagged_stream_multiply_length_0 = blocks.tagged_stream_multiply_length(gr.sizeof_gr_complex*1, "packet_len", (1.0/decim_fac))
        self.blocks_tagged_stream_multiply_length_0.set_min_output_buffer(min_out_buffer)
        # [DSP] multiply_conjugate_cc（乘以共轭：去斜/解调）
        # - 输入0：Tx（发射 FMCW）
        # - 输入1：Rx_noisy（回波+噪声）
        # - 输出：Tx * conj(Rx_noisy)（得到低频 beat 信号，包含距离/速度信息）
        self.blocks_multiply_conjugate_cc_0 = blocks.multiply_conjugate_cc(1)
        self.blocks_multiply_conjugate_cc_0.set_min_output_buffer(min_out_buffer)
        # [DSP] add_vcc（复数加法）
        # - 输入0：噪声
        # - 输入1：目标回波
        # - 输出：回波 + 噪声
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        self.blocks_add_xx_0.set_min_output_buffer(min_out_buffer)
        # [Source] noise_source_c（复高斯白噪声）
        # - 输出：complex noise
        # - 参数：高斯噪声，幅度 0.1
        self.analog_noise_source_x_0 = analog.noise_source_c(analog.GR_GAUSSIAN, 0.1, 0)
        self.analog_noise_source_x_0.set_min_output_buffer(min_out_buffer)


        ##################################################
        # Connections
        # Connections 就是“线”，定义了端口级的数据流（按这里读，就等价于按 GRC 图从左到右走一遍）。
        ##################################################
        # 数据流：analog_noise_source_x_0[0] -> blocks_add_xx_0[0]  (噪声 -> 加法器(输入0))
        self.connect((self.analog_noise_source_x_0, 0), (self.blocks_add_xx_0, 0))
        # 数据流：blocks_add_xx_0[0] -> blocks_multiply_conjugate_cc_0[1]  (带噪回波 -> 乘共轭(端口1))
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_multiply_conjugate_cc_0, 1))
        # 数据流：blocks_multiply_conjugate_cc_0[0] -> rational_resampler_xxx_0[0]  (beat -> 降采样)
        self.connect((self.blocks_multiply_conjugate_cc_0, 0), (self.rational_resampler_xxx_0, 0))
        # 数据流：blocks_tagged_stream_multiply_length_0[0] -> radar_split_cc_0[0]  (整帧 beat -> 分段)
        self.connect((self.blocks_tagged_stream_multiply_length_0, 0), (self.radar_split_cc_0, 0))
        # 数据流：blocks_tagged_stream_multiply_length_0[0] -> radar_split_cc_0_0[0]  (整帧 beat -> 分段)
        self.connect((self.blocks_tagged_stream_multiply_length_0, 0), (self.radar_split_cc_0_0, 0))
        # 数据流：blocks_tagged_stream_multiply_length_0[0] -> radar_split_cc_0_0_0[0]  (整帧 beat -> 分段)
        self.connect((self.blocks_tagged_stream_multiply_length_0, 0), (self.radar_split_cc_0_0_0, 0))
        # 数据流：blocks_throttle_0[0] -> radar_static_target_simulator_cc_0[0]  (Throttle输出 -> 目标仿真器)
        self.connect((self.blocks_throttle_0, 0), (self.radar_static_target_simulator_cc_0, 0))
        # 数据流：radar_signal_generator_fmcw_c_0[0] -> blocks_multiply_conjugate_cc_0[0]  (Tx -> 乘共轭(端口0))
        self.connect((self.radar_signal_generator_fmcw_c_0, 0), (self.blocks_multiply_conjugate_cc_0, 0))
        # 数据流：radar_signal_generator_fmcw_c_0[0] -> blocks_throttle_0[0]  (Tx -> Throttle)
        self.connect((self.radar_signal_generator_fmcw_c_0, 0), (self.blocks_throttle_0, 0))
        # 数据流：radar_split_cc_0[0] -> qtgui_sink_x_0[0]  (分段 -> GUI 显示)
        self.connect((self.radar_split_cc_0, 0), (self.qtgui_sink_x_0, 0))
        # 数据流：radar_split_cc_0[0] -> radar_ts_fft_cc_0[0]  (分段 -> FFT)
        self.connect((self.radar_split_cc_0, 0), (self.radar_ts_fft_cc_0, 0))
        # 数据流：radar_split_cc_0_0[0] -> qtgui_sink_x_0_0[0]  (分段 -> GUI 显示)
        self.connect((self.radar_split_cc_0_0, 0), (self.qtgui_sink_x_0_0, 0))
        # 数据流：radar_split_cc_0_0[0] -> radar_ts_fft_cc_0_0[0]  (分段 -> FFT)
        self.connect((self.radar_split_cc_0_0, 0), (self.radar_ts_fft_cc_0_0, 0))
        # 数据流：radar_split_cc_0_0_0[0] -> qtgui_sink_x_0_0_0[0]  (分段 -> GUI 显示)
        self.connect((self.radar_split_cc_0_0_0, 0), (self.qtgui_sink_x_0_0_0, 0))
        # 数据流：radar_split_cc_0_0_0[0] -> radar_ts_fft_cc_0_1[0]  (分段 -> FFT)
        self.connect((self.radar_split_cc_0_0_0, 0), (self.radar_ts_fft_cc_0_1, 0))
        # 数据流：radar_static_target_simulator_cc_0[0] -> blocks_add_xx_0[1]  (目标回波 -> 加法器(输入1))
        self.connect((self.radar_static_target_simulator_cc_0, 0), (self.blocks_add_xx_0, 1))
        # 数据流：radar_ts_fft_cc_0[0] -> radar_find_max_peak_c_0[0]  (频谱 -> 找峰值)
        self.connect((self.radar_ts_fft_cc_0, 0), (self.radar_find_max_peak_c_0, 0))
        # 数据流：radar_ts_fft_cc_0_0[0] -> radar_find_max_peak_c_0_0[0]  (频谱 -> 找峰值)
        self.connect((self.radar_ts_fft_cc_0_0, 0), (self.radar_find_max_peak_c_0_0, 0))
        # 数据流：radar_ts_fft_cc_0_1[0] -> radar_find_max_peak_c_0_0_0[0]  (频谱 -> 找峰值)
        self.connect((self.radar_ts_fft_cc_0_1, 0), (self.radar_find_max_peak_c_0_0_0, 0))
        # 数据流：rational_resampler_xxx_0[0] -> blocks_tagged_stream_multiply_length_0[0]  (修正 tag 前的流)
        self.connect((self.rational_resampler_xxx_0, 0), (self.blocks_tagged_stream_multiply_length_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "simulator_fmcw")
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

    # # set_samp_rate: 修改采样率时，需要同步很多块的参数
    # # - throttle 的 sample_rate
    # # - GUI 频率轴范围（0 ~ samp_rate/decim_fac）
    # # - 目标仿真器的内部采样率（setup_targets）
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

    # # set_velocity: GUI 速度滑块回调
    # # - 更新 self.velocity
    # # - 调用 static_target_simulator_cc_0.setup_targets(...) 把速度写进“目标模型”
    def set_velocity(self, velocity):
        self.velocity = velocity
        self.radar_static_target_simulator_cc_0.setup_targets([self.value_range], [self.velocity], [1e16], [0], [0], self.samp_rate, self.center_freq, -10, True, True)

    def get_value_range(self):
        return self.value_range

    # # set_value_range: GUI 距离滑块回调
    # # - 更新 self.value_range
    # # - 调用 setup_targets(...) 把距离写进“目标模型”
    def set_value_range(self, value_range):
        self.value_range = value_range
        self.radar_static_target_simulator_cc_0.setup_targets([self.value_range], [self.velocity], [1e16], [0], [0], self.samp_rate, self.center_freq, -10, True, True)

    def get_v_res(self):
        return self.v_res

    def set_v_res(self, v_res):
        self.v_res = v_res

    def get_threshold(self):
        return self.threshold

    # # set_threshold: GUI 门限滑块回调
    # # - 更新 self.threshold
    # # - 同步到 3 个 find_max_peak 块（CW/UP/DOWN）
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

    # # set_protect_samp: GUI protect_samp 滑块回调
    # # - 更新 self.protect_samp
    # # - 同步到 3 个 find_max_peak 块
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

    # # set_decim_fac: 修改降采样因子时
    # # - tagged_stream_multiply_length 的 scalar 要更新（1/decim_fac）
    # # - GUI 频率轴范围也要更新（因为有效采样率变了）
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