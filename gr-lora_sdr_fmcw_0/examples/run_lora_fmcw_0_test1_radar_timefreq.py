#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import signal
import subprocess
import sys
import time

# from plot_radar_and_mux_timefreq_fixed import plot_single_signal_timefreq


def remove_if_exists(path):
    try:
        os.remove(path)
    except FileNotFoundError:
        pass


def ensure_parent_dir(path):
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)


def stop_child(child):
    if child.poll() is not None:
        return child.returncode

    try:
        if child.stdin is not None and not child.stdin.closed:
            child.stdin.write("\n")
            child.stdin.flush()
    except BrokenPipeError:
        pass

    try:
        return child.wait(timeout=5.0)
    except subprocess.TimeoutExpired:
        child.send_signal(signal.SIGINT)
        try:
            return child.wait(timeout=5.0)
        except subprocess.TimeoutExpired:
            child.terminate()
            return child.wait(timeout=5.0)


def main():
    if len(sys.argv) not in (5, 6, 7):
        print(
            "usage: run_lora_fmcw_0_test1_radar_timefreq.py "
            "<python_exec> <flowgraph.py> <radar_rx.dat> <figure.png> [run_time_s] [sample_rate]",
            file=sys.stderr,
        )
        return 2

    python_exec, flowgraph_path, radar_rx_path, fig_path = sys.argv[1:5]
    run_time_s = float(sys.argv[5]) if len(sys.argv) >= 6 else 4.0
    sample_rate = float(sys.argv[6]) if len(sys.argv) >= 7 else 500000.0

    for path in (radar_rx_path, fig_path):
        remove_if_exists(path)
        ensure_parent_dir(path)

    child = None

    def forward_signal(sig, _frame):
        if child is not None and child.poll() is None:
            child.send_signal(sig)

    signal.signal(signal.SIGINT, forward_signal)
    signal.signal(signal.SIGTERM, forward_signal)

    print(f"[capture] radar rx dat -> {radar_rx_path}")
    print(f"[capture] figure       -> {fig_path}")
    print(f"[capture] run time     -> {run_time_s:.1f} s")

    child = subprocess.Popen(
        [python_exec, "-u", flowgraph_path],
        stdin=subprocess.PIPE,
        text=True,
    )

    t0 = time.time()
    last_size = 0
    while child.poll() is None and (time.time() - t0) < run_time_s:
        if os.path.exists(radar_rx_path):
            size = os.path.getsize(radar_rx_path)
            if size != last_size:
                print(f"[capture] radar rx bytes = {size}")
                last_size = size
        time.sleep(0.1)

    rc = stop_child(child)

    # Plotting is temporarily disabled so we can focus on flowgraph runtime behavior.
    if os.path.exists(radar_rx_path) and os.path.getsize(radar_rx_path) > 0:
        print("[plot] skipped: plotting disabled")
    else:
        print("[plot] skipped: radar rx capture file missing or empty")

    return rc


if __name__ == "__main__":
    raise SystemExit(main())
