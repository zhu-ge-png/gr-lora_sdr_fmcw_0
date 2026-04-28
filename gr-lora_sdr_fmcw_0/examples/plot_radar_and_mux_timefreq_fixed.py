#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os

os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib")

import numpy as np
import matplotlib
matplotlib.use("Agg")
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
    ax_if.plot(t, fi, linewidth=0.8)
    ax_if.set_title(title + ' instantaneous frequency')
    ax_if.set_xlabel('Time [s]')
    ax_if.set_ylabel('Freq [Hz]')
    ax_if.grid(True, alpha=0.3)


def plot_single_signal_timefreq(signal_path, fig_path, fs=500000.0, title='Radar RX accepted'):
    signal = read_c64(signal_path)

    fig, axs = plt.subplots(2, 1, figsize=(8, 8), constrained_layout=True)
    plot_one(axs[0], axs[1], signal, fs, title)
    fig.suptitle(title + ': time-frequency view')
    fig.savefig(fig_path, dpi=180)
    plt.close(fig)
    return signal.size


def main():
    parser = argparse.ArgumentParser(description='Plot FMCW time-frequency views from captured complex64 samples.')
    parser.add_argument('--signal', help='Single complex64 file to plot as spectrogram + instantaneous frequency.')
    parser.add_argument('--figure', help='Output figure path.')
    parser.add_argument('--sample-rate', type=float, default=500000.0, help='Sample rate in Hz.')
    parser.add_argument('--title', default='Radar RX accepted', help='Plot title for --signal mode.')
    parser.add_argument('--out-dir', default='/home/lmz/tmp/fmcw_obs', help='Default directory for legacy radar/mod plotting.')
    args = parser.parse_args()

    if args.signal:
        fig_path = args.figure or os.path.join(
            os.path.dirname(args.signal) or '.',
            'radar_rx_timefreq.png',
        )
        sample_count = plot_single_signal_timefreq(
            args.signal,
            fig_path,
            fs=args.sample_rate,
            title=args.title,
        )
        print(f"[plot] signal samples = {sample_count}")
        print(f"[plot] saved figure   -> {fig_path}")
        return

    fs = args.sample_rate
    out_dir = args.out_dir
    radar_path = os.path.join(out_dir, 'radar_out.dat')
    mod_path = os.path.join(out_dir, 'mod_out.dat')
    pseudo_mux_path = os.path.join(out_dir, 'pseudo_mux.dat')
    fig_path = args.figure or os.path.join(out_dir, 'radar_pseudomux_timefreq.png')

    radar = read_c64(radar_path)
    mod = read_c64(mod_path)

    # Build an offline "pseudo MUX" waveform by direct concatenation.
    pseudo_mux = np.concatenate([radar, mod]).astype(np.complex64)
    pseudo_mux.tofile(pseudo_mux_path)

    fig, axs = plt.subplots(2, 2, figsize=(14, 8), constrained_layout=True)
    plot_one(axs[0, 0], axs[1, 0], radar, fs, 'Radar output')
    plot_one(axs[0, 1], axs[1, 1], pseudo_mux, fs, 'Pseudo-MUX output')
    fig.suptitle('Radar output and pseudo-MUX output: time-frequency view')
    fig.savefig(fig_path, dpi=180)

    print(f"[plot] pseudo mux samples = {pseudo_mux.size}")
    print(f"[plot] saved pseudo mux dat -> {pseudo_mux_path}")
    print(f"[plot] saved figure         -> {fig_path}")


if __name__ == '__main__':
    main()
