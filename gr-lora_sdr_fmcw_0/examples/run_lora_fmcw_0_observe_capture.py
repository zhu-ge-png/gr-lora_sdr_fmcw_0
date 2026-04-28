#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import signal
import subprocess
import sys

os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib")

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def remove_if_exists(path):
    try:
        os.remove(path)
    except FileNotFoundError:
        pass


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
    ax_spec.set_title(title + " spectrogram")
    ax_spec.set_xlabel("Time [s]")
    ax_spec.set_ylabel("Freq [Hz]")

    fi = inst_freq_hz(x, fs)
    t = np.arange(fi.size) / fs
    ax_if.plot(t, fi, linewidth=0.8)
    ax_if.set_title(title + " instantaneous frequency")
    ax_if.set_xlabel("Time [s]")
    ax_if.set_ylabel("Freq [Hz]")
    ax_if.grid(True, alpha=0.3)


def save_timefreq_figure(radar_path, mux_path, fig_path, fs=500000.0):
    radar = read_c64(radar_path)
    mux = read_c64(mux_path)

    fig, axs = plt.subplots(2, 2, figsize=(14, 8), constrained_layout=True)
    plot_one(axs[0, 0], axs[1, 0], radar, fs, "Radar output")
    plot_one(axs[0, 1], axs[1, 1], mux, fs, "True MUX output")
    fig.suptitle("Radar output and true MUX output: time-frequency view")
    fig.savefig(fig_path, dpi=180)
    plt.close(fig)


def main():
    if len(sys.argv) != 6:
        print(
            "usage: run_lora_fmcw_0_observe_capture.py "
            "<python_exec> <flowgraph.py> <radar.dat> <mux.dat> <figure.png>",
            file=sys.stderr,
        )
        return 2

    python_exec, flowgraph_path, radar_path, mux_path, fig_path = sys.argv[1:]

    for stale_path in (radar_path, mux_path, fig_path):
        remove_if_exists(stale_path)

    child = None

    def forward_signal(sig, _frame):
        if child is not None and child.poll() is None:
            child.send_signal(sig)

    signal.signal(signal.SIGINT, forward_signal)
    signal.signal(signal.SIGTERM, forward_signal)

    print(f"[capture] radar dat -> {radar_path}")
    print(f"[capture] mux dat   -> {mux_path}")
    print(f"[capture] figure    -> {fig_path}")

    child = subprocess.Popen([python_exec, "-u", flowgraph_path])
    rc = child.wait()

    try:
        if os.path.exists(radar_path) and os.path.getsize(radar_path) > 0 and os.path.exists(mux_path) and os.path.getsize(mux_path) > 0:
            save_timefreq_figure(radar_path, mux_path, fig_path)
            print(f"[plot] saved true MUX time-frequency figure -> {fig_path}")
        else:
            print("[plot] skipped: captured dat file missing or empty")
    except Exception as exc:
        print(f"[plot] failed to save true MUX time-frequency figure: {exc}")

    return rc


if __name__ == "__main__":
    raise SystemExit(main())
