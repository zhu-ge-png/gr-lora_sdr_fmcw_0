#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from gnuradio import blocks, gr, radar
import gnuradio.lora_sdr_fmcw_0 as lora_sdr
import pmt
import os
import time

OUTDIR = "/home/lmz/tmp/fmcw_obs"
os.makedirs(OUTDIR, exist_ok=True)

class tb_obs(gr.top_block):
    def __init__(self):
        gr.top_block.__init__(self, "observe_tags_and_modout_fixed", catch_exceptions=True)

        bw = 125000
        sf = 7
        samp_rate = bw * 4
        preamb_len = 7
        sync_word = 0x12
        cr = 2
        has_crc = True
        impl_head = False
        frame_period_ms = 2000

        # Radar params; current generator maps to 2-symbol triangle mode internally.
        fmcw_up_len = 205
        fmcw_down_len = 205
        fmcw_cw_len = 102
        fmcw_freq_sweep = 0.90 * bw
        fmcw_freq_cw = -0.45 * bw

        # One 2-symbol triangle = 2 * (2^sf) * os_factor = 1024 samples at SF7/BW125k/os4.
        radar_samples = preamb_len * 2 * (2 ** sf) * (samp_rate // bw)   # 7 * 2 * 128 * 4 = 7168
        # MOD0 tag debug showed one complete frame_len = 25728.
        mod_samples = 25728

        radar_path = os.path.join(OUTDIR, "radar_out.dat")
        mod_path = os.path.join(OUTDIR, "mod_out.dat")
        for p in (radar_path, mod_path):
            try:
                os.remove(p)
            except FileNotFoundError:
                pass

        print(f"[observe] radar_out -> {radar_path}")
        print(f"[observe] mod_out   -> {mod_path}")
        print(f"[observe] radar samples = {radar_samples}, mod samples = {mod_samples}")
        print(f"[observe] pseudo mux total samples = {radar_samples + mod_samples}")

        # Sources / TX chain
        self.msg_strobe = blocks.message_strobe(pmt.intern("helloworld : 0"), frame_period_ms)
        self.payload_id_inc = lora_sdr.payload_id_inc(':')
        self.whitening = lora_sdr.whitening(True, True, ',', 'packet_len')
        self.header = lora_sdr.header(impl_head, has_crc, cr)
        self.add_crc = lora_sdr.add_crc(has_crc)
        self.hamming_enc = lora_sdr.hamming_enc(cr, sf)
        self.interleaver = lora_sdr.interleaver(cr, sf, 0, bw)
        self.gray_demap = lora_sdr.gray_demap(sf)
        self.modulate0 = lora_sdr.modulate0(sf, samp_rate, bw, [sync_word], 4096, preamb_len)
        self.modulate0.set_min_output_buffer(65536)

        self.radar_gen = radar.signal_generator_fmcw_c(
            samp_rate, fmcw_up_len, fmcw_down_len, fmcw_cw_len,
            fmcw_freq_cw, fmcw_freq_sweep, 1, preamb_len, "frame_len")

        # Tag viewers
        self.radar_tag_dbg = blocks.tag_debug(gr.sizeof_gr_complex, "RADAR", "frame_len")
        self.mod_tag_dbg   = blocks.tag_debug(gr.sizeof_gr_complex, "MOD0",  "frame_len")
        try:
            self.radar_tag_dbg.set_display(True)
            self.mod_tag_dbg.set_display(True)
        except Exception:
            pass

        # File capture
        self.radar_head = blocks.head(gr.sizeof_gr_complex, radar_samples)
        self.mod_head = blocks.head(gr.sizeof_gr_complex, mod_samples)
        self.radar_sink = blocks.file_sink(gr.sizeof_gr_complex, radar_path, False)
        self.mod_sink = blocks.file_sink(gr.sizeof_gr_complex, mod_path, False)
        self.radar_sink.set_unbuffered(True)
        self.mod_sink.set_unbuffered(True)

        # Message connections
        self.msg_connect((self.msg_strobe, 'strobe'), (self.payload_id_inc, 'msg_in'))
        self.msg_connect((self.msg_strobe, 'strobe'), (self.whitening, 'msg'))
        self.msg_connect((self.payload_id_inc, 'msg_out'), (self.msg_strobe, 'set_msg'))

        # Stream connections for modulate0 branch
        self.connect((self.whitening, 0), (self.header, 0))
        self.connect((self.header, 0), (self.add_crc, 0))
        self.connect((self.add_crc, 0), (self.hamming_enc, 0))
        self.connect((self.hamming_enc, 0), (self.interleaver, 0))
        self.connect((self.interleaver, 0), (self.gray_demap, 0))
        self.connect((self.gray_demap, 0), (self.modulate0, 0))

        # Observe radar tags + samples
        self.connect((self.radar_gen, 0), (self.radar_tag_dbg, 0))
        self.connect((self.radar_gen, 0), (self.radar_head, 0))
        self.connect((self.radar_head, 0), (self.radar_sink, 0))

        # Observe modulate0 tags + samples
        self.connect((self.modulate0, 0), (self.mod_tag_dbg, 0))
        self.connect((self.modulate0, 0), (self.mod_head, 0))
        self.connect((self.mod_head, 0), (self.mod_sink, 0))


def main():
    tb = tb_obs()
    tb.start()

    # Give the flowgraph enough time to emit one radar packet and one modulated frame.
    time.sleep(3.0)

    tb.stop()
    tb.wait()

    for name in ("radar_out.dat", "mod_out.dat"):
        path = os.path.join(OUTDIR, name)
        size = os.path.getsize(path) if os.path.exists(path) else 0
        print(f"[observe] {name}: {size} bytes")


if __name__ == '__main__':
    main()
