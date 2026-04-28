#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Improved time-frequency plotting for captured complex64 FMCW / Radar RX signals.

Compared with the original version:
- keeps the spectrogram, but overlays an STFT ridge
- replaces raw line-plot instantaneous frequency with:
    * magnitude-masked instantaneous frequency
    * scatter plotting instead of connecting every point
    * moving-average smoothing on the kept points
- preserves the original CLI shape and function names, so it can be used
  as a drop-in replacement if desired
"""

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


def moving_avg(y, k=21):
    y = np.asarray(y, dtype=float)
    if y.size < 3:
        return y.copy()

    k = int(k)
    if k < 3:
        return y.copy()
    if k > y.size:
        k = y.size if y.size % 2 == 1 else y.size - 1
    if k < 3:
        return y.copy()
    if k % 2 == 0:
        k -= 1
    if k < 3:
        return y.copy()

    kernel = np.ones(k, dtype=float) / k
    return np.convolve(y, kernel, mode="same")


def masked_inst_freq_hz(x, fs, mag_ratio=0.30, ref_percentile=95.0):
    """
    Estimate instantaneous frequency from adjacent-sample phase differences,
    but keep only points whose adjacent-product magnitude is sufficiently large.
    """
    if len(x) < 2:
        return (
            np.array([], dtype=float),
            np.array([], dtype=float),
            np.array([], dtype=float),
            0.0,
        )

    prod = x[1:] * np.conj(x[:-1])
    dphi = np.angle(prod)
    fi = dphi * fs / (2 * np.pi)
    mag = np.abs(prod)

    ref = np.percentile(mag, ref_percentile)
    ref = max(float(ref), 1e-12)
    th = mag_ratio * ref
    keep = mag >= th

    t = np.arange(fi.size, dtype=float) / fs
    return t[keep], fi[keep], mag[keep], th


def downsample_for_plot(t, y, max_points=5000):
    t = np.asarray(t)
    y = np.asarray(y)
    if t.size <= max_points:
        return t, y
    step = int(np.ceil(t.size / max_points))
    return t[::step], y[::step]


def robust_ylim(y, default_half_span):
    y = np.asarray(y, dtype=float)
    if y.size == 0:
        return (-default_half_span, default_half_span)

    lo = np.percentile(y, 1)
    hi = np.percentile(y, 99)
    if not np.isfinite(lo) or not np.isfinite(hi) or lo == hi:
        return (-default_half_span, default_half_span)

    pad = 0.10 * max(hi - lo, 1.0)
    return (lo - pad, hi + pad)


def plot_one(ax_spec, ax_if, x, fs, title):
    nfft = 256
    noverlap = 192

    # Spectrogram + ridge overlay
    pxx, freqs, bins, _ = ax_spec.specgram(
        x, NFFT=nfft, Fs=fs, noverlap=noverlap
    )
    ax_spec.set_title(title + " spectrogram + ridge")
    ax_spec.set_xlabel("Time [s]")
    ax_spec.set_ylabel("Freq [Hz]")

    if np.size(pxx) > 0:
        ridge_idx = np.argmax(pxx, axis=0)
        ridge_hz = freqs[ridge_idx]
        ridge_hz_smooth = moving_avg(ridge_hz, k=9)
        ax_spec.plot(bins, ridge_hz_smooth, linewidth=1.4, alpha=0.9)

    # Masked instantaneous frequency, scatter only
    t_if, fi_if, _mag_if, th = masked_inst_freq_hz(
        x, fs, mag_ratio=0.30, ref_percentile=95.0
    )

    if t_if.size > 0:
        t_plot, fi_plot = downsample_for_plot(t_if, fi_if, max_points=5000)
        fi_smooth = moving_avg(fi_plot, k=21)

        ax_if.scatter(t_plot, fi_plot, s=4, alpha=0.35)
        if fi_smooth.size > 0:
            ax_if.plot(t_plot, fi_smooth, linewidth=1.2, alpha=0.95)

    ax_if.set_title(title + f" masked instantaneous frequency (th={th:.3g})")
    ax_if.set_xlabel("Time [s]")
    ax_if.set_ylabel("Freq [Hz]")
    ax_if.grid(True, alpha=0.3)
    ax_if.set_ylim(*robust_ylim(fi_if, default_half_span=0.5 * fs))


def plot_single_signal_timefreq(signal_path, fig_path, fs=500000.0, title="Radar RX accepted"):
    signal = read_c64(signal_path)

    fig, axs = plt.subplots(2, 1, figsize=(8.5, 8.5), constrained_layout=True)
    plot_one(axs[0], axs[1], signal, fs, title)
    fig.suptitle(title + ": time-frequency view (ridge + masked IF)")
    fig.savefig(fig_path, dpi=180)
    plt.close(fig)
    return signal.size


def main():
    parser = argparse.ArgumentParser(
        description="Plot FMCW time-frequency views from captured complex64 samples."
    )
    parser.add_argument(
        "--signal",
        help="Single complex64 file to plot as spectrogram + masked instantaneous frequency.",
    )
    parser.add_argument("--figure", help="Output figure path.")
    parser.add_argument(
        "--sample-rate", type=float, default=500000.0, help="Sample rate in Hz."
    )
    parser.add_argument(
        "--title", default="Radar RX accepted", help="Plot title for --signal mode."
    )
    parser.add_argument(
        "--out-dir",
        default="/home/lmz/tmp/fmcw_obs",
        help="Default directory for legacy radar/mod plotting.",
    )
    args = parser.parse_args()

    if args.signal:
        fig_path = args.figure or os.path.join(
            os.path.dirname(args.signal) or ".",
            "radar_rx_timefreq_v2.png",
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
    radar_path = os.path.join(out_dir, "radar_out.dat")
    mod_path = os.path.join(out_dir, "mod_out.dat")
    pseudo_mux_path = os.path.join(out_dir, "pseudo_mux.dat")
    fig_path = args.figure or os.path.join(out_dir, "radar_pseudomux_timefreq_v2.png")

    radar = read_c64(radar_path)
    mod = read_c64(mod_path)

    # Build an offline "pseudo MUX" waveform by direct concatenation.
    pseudo_mux = np.concatenate([radar, mod]).astype(np.complex64)
    pseudo_mux.tofile(pseudo_mux_path)

    fig, axs = plt.subplots(2, 2, figsize=(14, 8.5), constrained_layout=True)
    plot_one(axs[0, 0], axs[1, 0], radar, fs, "Radar output")
    plot_one(axs[0, 1], axs[1, 1], pseudo_mux, fs, "Pseudo-MUX output")
    fig.suptitle("Radar output and pseudo-MUX output: time-frequency view (ridge + masked IF)")
    fig.savefig(fig_path, dpi=180)
    plt.close(fig)

    print(f"[plot] pseudo mux samples = {pseudo_mux.size}")
    print(f"[plot] saved pseudo mux dat -> {pseudo_mux_path}")
    print(f"[plot] saved figure         -> {fig_path}")


if __name__ == "__main__":
    main()