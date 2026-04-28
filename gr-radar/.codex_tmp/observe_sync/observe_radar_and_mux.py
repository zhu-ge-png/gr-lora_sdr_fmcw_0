#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import time

import pmt
from gnuradio import blocks, gr, radar
import gnuradio.lora_sdr_fmcw_0 as lora_sdr


def remove_if_exists(path):
    try:
        os.remove(path)
    except FileNotFoundError:
        pass


class observe_radar_and_mux(gr.top_block):
    def __init__(self,
                 out_dir="/home/lmz/tmp/fmcw_obs",
                 sf=7,
                 bw=125000,
                 samp_rate=None,
                 preamb_len=8,
                 sync_word=0x12,
                 has_crc=True,
                 impl_head=False,
                 cr=2,
                 pay_len=255,
                 frame_period_ms=2000,
                 center_freq=2400e6,
                 radar_capture_samples=None,
                 mod_capture_samples=None,
                 mux_capture_samples=None,
                 rx_capture_samples=None,
                 frame_sync_capture_samples=None):
        gr.top_block.__init__(self, "observe_radar_and_mux", catch_exceptions=True)

        if samp_rate is None:
            samp_rate = bw * 4

        os.makedirs(out_dir, exist_ok=True)
        self.out_dir = out_dir

        self.radar_path = os.path.join(out_dir, "radar_out.dat")
        self.mod_path = os.path.join(out_dir, "mod_out.dat")
        self.mux_path = os.path.join(out_dir, "mux_out.dat")
        self.rx_path = os.path.join(out_dir, "rx_in.dat")
        self.frame_sync_path = os.path.join(out_dir, "frame_sync0_out.dat")
        self.meta_path = os.path.join(out_dir, "capture_meta.json")

        for stale_path in (
            self.radar_path,
            self.mod_path,
            self.mux_path,
            self.rx_path,
            self.frame_sync_path,
            self.meta_path,
            os.path.join(out_dir, "observe_timefreq_all.png"),
            os.path.join(out_dir, "observe_timefreq_boundary_zoom.png"),
        ):
            remove_if_exists(stale_path)

        self.sf = sf
        self.bw = bw
        self.samp_rate = samp_rate
        self.preamb_len = preamb_len
        self.sync_word = sync_word
        self.has_crc = has_crc
        self.impl_head = impl_head
        self.cr = cr
        self.pay_len = pay_len
        self.frame_period_ms = frame_period_ms
        self.center_freq = center_freq
        self.sps = int((2 ** sf) * samp_rate / bw)

        self.radar_capture_samples = radar_capture_samples or (preamb_len * 2 * self.sps)
        self.mod_capture_samples = mod_capture_samples or 40000
        self.mux_capture_samples = mux_capture_samples or (self.radar_capture_samples + self.mod_capture_samples)
        self.rx_capture_samples = rx_capture_samples or self.mux_capture_samples
        self.frame_sync_capture_samples = frame_sync_capture_samples or (12 * self.sps)

        self.fmcw_up_len = 205
        self.fmcw_down_len = 205
        self.fmcw_cw_len = 102
        self.fmcw_freq_cw = -0.45 * bw
        self.fmcw_freq_sweep = 0.90 * bw
        self.soft_decoding = False

        self.radar_signal_generator_fmcw_c_0 = radar.signal_generator_fmcw_c(
            samp_rate,
            self.fmcw_up_len,
            self.fmcw_down_len,
            self.fmcw_cw_len,
            self.fmcw_freq_cw,
            self.fmcw_freq_sweep,
            1,
            preamb_len,
            "frame_len",
            sf,
            bw,
        )
        self.radar_signal_generator_fmcw_c_0.set_min_output_buffer(16384)

        self.lora_sdr_whitening_0_0 = lora_sdr.whitening(True, True, ',', 'packet_len')
        self.lora_sdr_payload_id_inc_0 = lora_sdr.payload_id_inc(':')
        self.lora_sdr_interleaver_0_0 = lora_sdr.interleaver(cr, sf, 0, bw)
        self.lora_sdr_header_decoder_0 = lora_sdr.header_decoder(impl_head, cr, pay_len, has_crc, 2, True)
        self.lora_sdr_header_0_0 = lora_sdr.header(impl_head, has_crc, cr)
        self.lora_sdr_hamming_enc_0_0 = lora_sdr.hamming_enc(cr, sf)
        self.lora_sdr_hamming_dec_0 = lora_sdr.hamming_dec(self.soft_decoding)
        self.lora_sdr_gray_mapping_0 = lora_sdr.gray_mapping(self.soft_decoding)
        self.lora_sdr_gray_demap_0_0 = lora_sdr.gray_demap(sf)
        self.lora_sdr_fmcw_0_modulate0_0 = lora_sdr.modulate0(sf, samp_rate, bw, [sync_word], 4096, preamb_len)
        self.lora_sdr_fmcw_0_modulate0_0.set_min_output_buffer(65536)
        self.lora_sdr_fmcw_0_frame_sync0_0 = lora_sdr.frame_sync0(int(center_freq), bw, sf, impl_head, [sync_word], 4, preamb_len)
        self.lora_sdr_fft_demod_0 = lora_sdr.fft_demod(self.soft_decoding, False)
        self.lora_sdr_dewhitening_0 = lora_sdr.dewhitening()
        self.lora_sdr_deinterleaver_0 = lora_sdr.deinterleaver(self.soft_decoding)
        self.lora_sdr_crc_verif_0 = lora_sdr.crc_verif(1, False)
        self.lora_sdr_add_crc_0_0 = lora_sdr.add_crc(has_crc)

        self.blocks_throttle2_0 = blocks.throttle(
            gr.sizeof_gr_complex * 1,
            samp_rate,
            True,
            0 if "auto" == "auto" else max(int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1),
        )
        self.blocks_tagged_stream_mux_0 = blocks.tagged_stream_mux(gr.sizeof_gr_complex * 1, 'frame_len', 0)
        self.blocks_tagged_stream_mux_0.set_min_output_buffer(2097152)
        self.blocks_message_strobe_0_0_0 = blocks.message_strobe(pmt.intern("helloworld : 0"), frame_period_ms)

        self.blocks_head_radar_0 = blocks.head(gr.sizeof_gr_complex * 1, self.radar_capture_samples)
        self.blocks_head_mod_0 = blocks.head(gr.sizeof_gr_complex * 1, self.mod_capture_samples)
        self.blocks_head_mux_0 = blocks.head(gr.sizeof_gr_complex * 1, self.mux_capture_samples)
        self.blocks_head_rx_0 = blocks.head(gr.sizeof_gr_complex * 1, self.rx_capture_samples)
        self.blocks_head_frame_sync_0 = blocks.head(gr.sizeof_gr_complex * 1, self.frame_sync_capture_samples)

        self.blocks_file_sink_radar_0 = blocks.file_sink(gr.sizeof_gr_complex * 1, self.radar_path, False)
        self.blocks_file_sink_mod_0 = blocks.file_sink(gr.sizeof_gr_complex * 1, self.mod_path, False)
        self.blocks_file_sink_mux_0 = blocks.file_sink(gr.sizeof_gr_complex * 1, self.mux_path, False)
        self.blocks_file_sink_rx_0 = blocks.file_sink(gr.sizeof_gr_complex * 1, self.rx_path, False)
        self.blocks_file_sink_frame_sync_0 = blocks.file_sink(gr.sizeof_gr_complex * 1, self.frame_sync_path, False)

        for sink in (
            self.blocks_file_sink_radar_0,
            self.blocks_file_sink_mod_0,
            self.blocks_file_sink_mux_0,
            self.blocks_file_sink_rx_0,
            self.blocks_file_sink_frame_sync_0,
        ):
            sink.set_unbuffered(True)

        self.msg_connect((self.blocks_message_strobe_0_0_0, 'strobe'), (self.lora_sdr_payload_id_inc_0, 'msg_in'))
        self.msg_connect((self.blocks_message_strobe_0_0_0, 'strobe'), (self.lora_sdr_whitening_0_0, 'msg'))
        self.msg_connect((self.lora_sdr_header_decoder_0, 'frame_info'), (self.lora_sdr_fmcw_0_frame_sync0_0, 'frame_info'))
        self.msg_connect((self.lora_sdr_payload_id_inc_0, 'msg_out'), (self.blocks_message_strobe_0_0_0, 'set_msg'))

        self.connect((self.blocks_throttle2_0, 0), (self.lora_sdr_fmcw_0_frame_sync0_0, 0))
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

        self.connect((self.radar_signal_generator_fmcw_c_0, 0), (self.blocks_head_radar_0, 0))
        self.connect((self.blocks_head_radar_0, 0), (self.blocks_file_sink_radar_0, 0))

        self.connect((self.lora_sdr_fmcw_0_modulate0_0, 0), (self.blocks_head_mod_0, 0))
        self.connect((self.blocks_head_mod_0, 0), (self.blocks_file_sink_mod_0, 0))

        self.connect((self.blocks_tagged_stream_mux_0, 0), (self.blocks_head_mux_0, 0))
        self.connect((self.blocks_head_mux_0, 0), (self.blocks_file_sink_mux_0, 0))

        self.connect((self.blocks_throttle2_0, 0), (self.blocks_head_rx_0, 0))
        self.connect((self.blocks_head_rx_0, 0), (self.blocks_file_sink_rx_0, 0))

        self.connect((self.lora_sdr_fmcw_0_frame_sync0_0, 0), (self.blocks_head_frame_sync_0, 0))
        self.connect((self.blocks_head_frame_sync_0, 0), (self.blocks_file_sink_frame_sync_0, 0))

    def write_meta(self):
        meta = {
            "samp_rate": self.samp_rate,
            "bw": self.bw,
            "sf": self.sf,
            "sps": self.sps,
            "sync_word": self.sync_word,
            "preamb_len": self.preamb_len,
            "has_crc": self.has_crc,
            "impl_head": self.impl_head,
            "cr": self.cr,
            "pay_len": self.pay_len,
            "frame_period_ms": self.frame_period_ms,
            "fmcw_up_len": self.fmcw_up_len,
            "fmcw_down_len": self.fmcw_down_len,
            "fmcw_cw_len": self.fmcw_cw_len,
            "fmcw_freq_cw": self.fmcw_freq_cw,
            "fmcw_freq_sweep": self.fmcw_freq_sweep,
            "radar_capture_samples": self.radar_capture_samples,
            "mod_capture_samples": self.mod_capture_samples,
            "mux_capture_samples": self.mux_capture_samples,
            "rx_capture_samples": self.rx_capture_samples,
            "frame_sync_capture_samples": self.frame_sync_capture_samples,
            "radar_file": self.radar_path,
            "mod_file": self.mod_path,
            "mux_file": self.mux_path,
            "rx_file": self.rx_path,
            "frame_sync_file": self.frame_sync_path,
        }
        with open(self.meta_path, "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2)


def wait_for_file_size(path, min_bytes, timeout_s):
    t0 = time.time()
    while time.time() - t0 < timeout_s:
        if os.path.exists(path) and os.path.getsize(path) >= min_bytes:
            return True
        time.sleep(0.1)
    return False


def report_capture(path, min_bytes, timeout_s):
    ok = wait_for_file_size(path, min_bytes, timeout_s)
    size = os.path.getsize(path) if os.path.exists(path) else 0
    return ok, size


def main():
    out_dir = "/home/lmz/tmp/fmcw_obs"
    tb = observe_radar_and_mux(out_dir=out_dir)
    tb.write_meta()

    needs = {
        "radar_out": (tb.radar_path, tb.radar_capture_samples * 8),
        "mod_out": (tb.mod_path, tb.mod_capture_samples * 8),
        "mux_out": (tb.mux_path, tb.mux_capture_samples * 8),
        "rx_in": (tb.rx_path, tb.rx_capture_samples * 8),
        "frame_sync0_out": (tb.frame_sync_path, max(tb.frame_sync_capture_samples // 2, 1) * 8),
    }

    print(f"[observe] out_dir = {out_dir}")
    for name, (path, need_bytes) in needs.items():
        print(f"[observe] {name:<15} -> {path} (need >= {need_bytes} bytes)")

    tb.start()
    results = {}
    for name, (path, need_bytes) in needs.items():
        results[name] = report_capture(path, need_bytes, 12.0)
    tb.stop()
    tb.wait()

    for name, (ok, size) in results.items():
        print(f"[observe] {name:<15} {'OK' if ok else 'TIMEOUT'} size={size}")


if __name__ == '__main__':
    main()
