#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import numpy as np
import matplotlib.pyplot as plt


def read_c64(path):
    x = np.fromfile(path, dtype=np.complex64)
    if x.size == 0:
        raise RuntimeError(f"No samples found in {path}")
    return x


def inst_freq_hz(x, fs):
    if len(x) < 2:
        return np.array([], dtype=float)
    dphi = np.angle(x[1:] * np.conj(x[:-1]))
    return dphi * fs / (2 * np.pi)


def plot_one(ax_spec, ax_if, x, fs, title):
    nfft = 256
    noverlap = 192
    ax_spec.specgram(x, NFFT=nfft, Fs=fs, noverlap=noverlap)
    ax_spec.set_title(title + ' spectrogram')
    ax_spec.set_xlabel('Time [s]')
    ax_spec.set_ylabel('Freq [Hz]')

    fi = inst_freq_hz(x, fs)
    t = np.arange(fi.size) / fs
    ax_if.plot(t, fi)
    ax_if.set_title(title + ' instantaneous frequency')
    ax_if.set_xlabel('Time [s]')
    ax_if.set_ylabel('Freq [Hz]')
    ax_if.grid(True, alpha=0.3)


def main():
    fs = 500000.0
    out_dir = "/home/lmz/tmp/fmcw_obs"
    radar_path = os.path.join(out_dir, 'radar_out.dat')
    mux_path = os.path.join(out_dir, 'mux_out.dat')
    fig_path = os.path.join(out_dir, 'radar_mux_timefreq.png')

    radar = read_c64(radar_path)
    mux = read_c64(mux_path)

    fig, axs = plt.subplots(2, 2, figsize=(14, 8), constrained_layout=True)
    plot_one(axs[0, 0], axs[1, 0], radar, fs, 'Radar output')
    plot_one(axs[0, 1], axs[1, 1], mux, fs, 'MUX output')
    fig.suptitle('Radar output and MUX output: time-frequency view')
    fig.savefig(fig_path, dpi=180)
    print(f"[plot] saved -> {fig_path}")


if __name__ == '__main__':
    main()
