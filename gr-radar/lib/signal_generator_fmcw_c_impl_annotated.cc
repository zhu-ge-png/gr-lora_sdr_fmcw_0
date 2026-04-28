/* -*- c++ -*- */
/*
 * Copyright 2014 Communications Engineering Lab, KIT.
 *
 * 这个文件实现了一个 GNU Radio 自定义同步块：signal_generator_fmcw_c。
 *
 * 作用：
 *   连续输出一个周期性重复的 FMCW 基带复信号包，每个包由三段组成：
 *     1) CW      （连续单频段）
 *     2) Up-chirp（上扫频段）
 *     3) Down-chirp（下扫频段）
 *
 * 在你的 GRC 流程图里，这个块就是左下角的 “Signal Generator FMCW”。
 * 它输出的是“发射参考波形”/“本振参考波形”，后面会：
 *   - 一路送入 Static Target Simulator，生成目标回波；
 *   - 另一路送入 Multiply Conjugate，与回波做拍频（dechirp / stretch processing）。
 *
 * 这个块的核心思想不是“直接存一串 IQ 样本”，
 * 而是先存“每个采样点对应的瞬时频率”，再在 work() 中逐点积分相位，
 * 从而生成连续相位的复指数信号： amplitude * exp(j*phase)。
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include "signal_generator_fmcw_c_impl.h"
#include <gnuradio/io_signature.h>
#include <gnuradio/math.h>

namespace gr {
namespace radar {

/*
 * 工厂函数：对外暴露的创建接口。
 *
 * 参数含义：
 *   samp_rate   : 输出采样率（Hz）
 *   samp_up     : 上扫频段占用的采样点数
 *   samp_down   : 下扫频段占用的采样点数
 *   samp_cw     : CW 段占用的采样点数
 *   freq_cw     : CW 中心频率 / 扫频起始频率（基带等效频率，Hz）
 *   freq_sweep  : 扫频带宽（Hz）
 *   amplitude   : 输出复信号幅度
 *   len_key     : tag 名称，通常为 packet_len
 *
 * 返回：
 *   一个指向实际实现类 signal_generator_fmcw_c_impl 的智能指针。
 */
signal_generator_fmcw_c::sptr signal_generator_fmcw_c::make(const int samp_rate,
                                                            const int samp_up,
                                                            const int samp_down,
                                                            const int samp_cw,
                                                            const float freq_cw,
                                                            const float freq_sweep,
                                                            const float amplitude,
                                                            const std::string& len_key)
{
    return gnuradio::make_block_sptr<signal_generator_fmcw_c_impl>(
        samp_rate, samp_up, samp_down, samp_cw, freq_cw, freq_sweep, amplitude, len_key);
}

/*
 * 构造函数：完成参数保存、包长计算、tag 初始化，以及“频率模板”生成。
 *
 * 注意：
 *   d_waveform 里存的不是 IQ 样本，而是“每个采样点对应的瞬时频率”。
 *   后续在 work() 中再把频率积分成相位，最后输出 exp(j*phase)。
 */
signal_generator_fmcw_c_impl::signal_generator_fmcw_c_impl(const int samp_rate,
                                                           const int samp_up,
                                                           const int samp_down,
                                                           const int samp_cw,
                                                           const float freq_cw,
                                                           const float freq_sweep,
                                                           const float amplitude,
                                                           const std::string& len_key)
    : gr::sync_block("signal_generator_fmcw_c",
                     // 该块没有输入端口：它是一个纯信号源
                     gr::io_signature::make(0, 0, 0),
                     // 只有一个输出端口，输出类型为 gr_complex
                     gr::io_signature::make(1, 1, sizeof(gr_complex))),
      d_samp_rate(samp_rate),
      d_samp_up(samp_up),
      d_samp_down(samp_down),
      d_samp_cw(samp_cw),
      d_freq_cw(freq_cw),
      d_freq_sweep(freq_sweep),
      d_amplitude(amplitude),
      // 一个完整 FMCW 包的长度 = CW 段 + 上扫段 + 下扫段
      d_packet_len(samp_up + samp_down + samp_cw),
      // 把字符串 tag 名转换成 PMT symbol，供 GNU Radio tag 机制使用
      d_key_len(pmt::string_to_symbol(len_key)),
      // 对应 tag 的值：这里直接写整个 packet 的长度
      d_value_len(pmt::from_long(d_packet_len)),
      // tag 的来源 ID，便于调试时识别是谁打的 tag
      d_srcid(pmt::string_to_symbol("sig_gen_fmcw")),
      // 当前输出到包内第几个采样点
      d_wv_counter(0),
      // 先把整段频率模板初始化为 freq_cw
      // 也就是说，默认全部先看成 CW 段
      d_waveform(d_packet_len, freq_cw)
{
    /*
     * 频率模板构造：
     *
     * 整个 packet 的排列顺序是：
     *   [0,                d_samp_cw-1]                -> CW
     *   [d_samp_cw,        d_samp_cw+d_samp_up-1]      -> Up-chirp
     *   [d_samp_cw+d_samp_up, 末尾]                    -> Down-chirp
     *
     * 其中：
     *   - CW 段频率恒为 d_freq_cw
     *   - Up-chirp 从 d_freq_cw 线性上升到 d_freq_cw + d_freq_sweep
     *   - Down-chirp 从 d_freq_cw + d_freq_sweep 线性下降回 d_freq_cw
     */

    // 生成上扫频段的“瞬时频率”序列
    for (int k = 0; k < d_samp_up; k++) {
        d_waveform[k + d_samp_cw] = d_freq_cw + (d_freq_sweep / (float)d_samp_up) * k;
    }

    // 生成下扫频段的“瞬时频率”序列
    for (int k = 0; k < d_samp_down; k++) {
        d_waveform[k + d_samp_cw + d_samp_up] =
            d_freq_cw + d_freq_sweep - (d_freq_sweep / (float)d_samp_down) * k;
    }
}

signal_generator_fmcw_c_impl::~signal_generator_fmcw_c_impl() {}

/*
 * work()：GNU Radio 调度器每次调用这个函数，让该块产出 noutput_items 个采样点。
 *
 * 处理流程：
 *   1. 逐点检查是否到达一个新 packet 的起点；如果是，则打 packet_len tag。
 *   2. 根据当前相位 d_phase 输出一个复指数采样点。
 *   3. 利用当前瞬时频率 d_waveform[d_wv_counter] 更新相位。
 *   4. 递增包内计数器，进入下一个采样点。
 */
int signal_generator_fmcw_c_impl::work(int noutput_items,
                                       gr_vector_const_void_star& input_items,
                                       gr_vector_void_star& output_items)
{
    gr_complex* out = (gr_complex*)output_items[0];

    // 注意：这个块没有输入，因此 input_items 没有实际用途。
    (void)input_items;

    /*
     * 逐点生成 IQ 信号。
     *
     * 输出模型：
     *   s[n] = A * exp(j*phase[n])
     *
     * 相位递推：
     *   phase[n+1] = phase[n] + 2*pi*f[n]/Fs
     *
     * 这正是“由瞬时频率积分得到相位”的离散形式。
     */
    for (int i = 0; i < noutput_items; i++) {
        /*
         * 当输出总索引恰好落在某个 packet 的起点时：
         *   - 给该采样点打上 packet_len tag；
         *   - 把包内频率索引 d_wv_counter 清零；
         *
         * 这样，下游 Tagged Stream 相关模块就知道：
         * “从这里开始，有一个长度为 d_packet_len 的完整 FMCW 包”。
         */
        if ((nitems_written(0) + i) % d_packet_len == 0) {
            add_item_tag(0, nitems_written(0) + i, d_key_len, d_value_len, d_srcid);
            d_wv_counter = 0;
        }

        // 用当前相位产生一个复数采样点：A * e^(j*phase)        一次写一个复数样本，循环很多次，最终组成模块输出端口上的 复数 IQ 流
        *out++ = d_amplitude * exp(d_phase);//Aejϕ即A(cosϕ+jsinϕ)

        /*
         * 更新相位：
         *
         * imag(d_phase) 当前被当作“相位值（弧度）”来使用。
         * 每前进一步，就加上当前采样点对应的相位增量：
         *     2*pi*f/Fs
         *
         * 再用 fmod(..., 2*pi) 把相位限制到 [0, 2*pi) 附近，
         * 避免相位无限增长。
         *
         * 这里把 d_phase 写成 gr_complex(0, phase)，是一个“内部相位状态变量”
         * 本质上就是在保存 j*phase，方便后面直接调用 exp(d_phase)。
         */
        //根据当前采样点对应的瞬时频率，更新下一时刻的相位 φ，并把相位限制在 0 ~ 2π 之间。
        d_phase =
            gr_complex(0,
                       std::fmod(imag(d_phase) + 2 * GR_M_PI * d_waveform[d_wv_counter] /
                                                     (float)d_samp_rate,
                                 2 * GR_M_PI));
        //imag(d_phase)：取出 d_phase 的虚部，取出来的其实就是当前相位 
        //d_waveform[d_wv_counter]当前采样点对应的瞬时频率，也就是说，d_waveform 这个数组里存的不是 IQ 点，而是每个时刻应该使用的频率值。


        // 包内样本索引前进一位，准备读取下一个瞬时频率
        d_wv_counter++;//最大为d_packet_len−1
    }

    // 告诉 GNU Radio：本次确实输出了 noutput_items 个样本
    return noutput_items;
}

} /* namespace radar */
} /* namespace gr */
