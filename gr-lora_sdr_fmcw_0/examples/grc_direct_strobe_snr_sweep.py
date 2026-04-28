#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import csv
import math
import os
import re
import select
import shlex
import subprocess
import sys
import tempfile
import time
from pathlib import Path


THIS_FILE = Path(__file__).resolve()
DEFAULT_GRC = THIS_FILE.with_name("lora_fmcw_0_test1.grc")
DEFAULT_CSV = THIS_FILE.with_name("lora_fmcw_0_test1_grc_direct_strobe_snr_vs_decoded_frames.csv")
DEFAULT_PNG = THIS_FILE.with_name("lora_fmcw_0_test1_grc_direct_strobe_snr_vs_decoded_frames.png")

TX_RE = re.compile(r"\[frame_id_tracker tx\] id=(-?\d+|\?)")
RX_RE = re.compile(r"\[frame_id_tracker rx\] id=(-?\d+|\?) status=(ok|bad)")

os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run the GRC-generated flowgraph directly, changing only SNRdB."
    )
    parser.add_argument("--grc", type=Path, default=DEFAULT_GRC)
    parser.add_argument("--start-snr", type=float, default=-10.0)
    parser.add_argument("--stop-snr", type=float, default=10.0)
    parser.add_argument("--step", type=float, default=0.5)
    parser.add_argument("--frames", type=int, default=100)
    parser.add_argument("--rx-grace", type=float, default=5.0)
    parser.add_argument("--max-extra-wait", type=float, default=30.0)
    parser.add_argument("--csv", type=Path, default=DEFAULT_CSV)
    parser.add_argument("--png", type=Path, default=DEFAULT_PNG)
    return parser.parse_args()


def frange(start, stop, step):
    if step <= 0:
        raise ValueError("step must be positive")
    count = int(round((stop - start) / step))
    if not math.isclose(start + count * step, stop, abs_tol=1e-9):
        raise ValueError("stop must align with start and step")
    return [round(start + idx * step, 10) for idx in range(count + 1)]


def set_grc_snr(source, snr_db):
    pattern = re.compile(
        r"(- name: SNRdB\n"
        r"  id: variable\n"
        r"  parameters:\n"
        r"    comment: .*\n"
        r"    value: ')[^']*(')",
        re.MULTILINE,
    )
    updated, count = pattern.subn(rf"\g<1>{snr_db:g}\2", source, count=1)
    if count != 1:
        raise RuntimeError("Could not update SNRdB in GRC file")
    return updated


def generate_flowgraph(grc_path, output_dir):
    subprocess.run(["grcc", "-o", str(output_dir), str(grc_path)], check=True)
    generated = output_dir / f"{grc_path.stem}.py"
    if not generated.exists():
        raise RuntimeError(f"grcc did not generate {generated}")
    return generated


def run_generated_flowgraph(py_path, frames, rx_grace, max_extra_wait):
    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"
    start_time = time.monotonic()
    tx_ids = []
    ok_ids = set()
    bad_crc_ids = []
    stop_requested_at = None
    command = [sys.executable, "-u", str(py_path)]

    proc = subprocess.Popen(
        command,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        bufsize=1,
        env=env,
    )

    try:
        while True:
            now = time.monotonic()
            if proc.poll() is not None:
                break
            if stop_requested_at is not None and now - stop_requested_at >= rx_grace:
                break
            if now - start_time >= frames + max_extra_wait:
                break

            ready, _, _ = select.select([proc.stdout], [], [], 0.2)
            if not ready:
                continue

            line = proc.stdout.readline()
            if not line:
                continue

            tx_match = TX_RE.search(line)
            if tx_match and tx_match.group(1) != "?":
                if len(tx_ids) < frames:
                    tx_ids.append(int(tx_match.group(1)))
                if len(tx_ids) >= frames and stop_requested_at is None:
                    stop_requested_at = time.monotonic()

            rx_match = RX_RE.search(line)
            if rx_match and rx_match.group(1) != "?":
                frame_id = int(rx_match.group(1))
                if rx_match.group(2) == "ok":
                    ok_ids.add(frame_id)
                else:
                    bad_crc_ids.append(frame_id)

        if proc.stdin:
            proc.stdin.write("\n")
            proc.stdin.flush()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.wait()
    finally:
        if proc.poll() is None:
            proc.terminate()

    expected = set(tx_ids)
    frames_ok = len(ok_ids & expected)
    frames_bad_crc = len([frame_id for frame_id in bad_crc_ids if frame_id in expected])
    frames_sent = len(tx_ids)
    return {
        "frames_sent": frames_sent,
        "frames_ok": frames_ok,
        "frames_bad_crc": frames_bad_crc,
        "frames_lost": frames_sent - frames_ok,
        "elapsed_s": round(time.monotonic() - start_time, 3),
    }


def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "snr_db",
        "frames_sent",
        "frames_ok",
        "frames_bad_crc",
        "frames_lost",
        "elapsed_s",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row[key] for key in fieldnames})


def write_plot(path, rows, frames):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    x_values = [row["snr_db"] for row in rows]
    y_values = [row["frames_ok"] for row in rows]
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(x_values, y_values, marker="o", linewidth=1.8, markersize=3.5)
    ax.set_xlabel("SNR (dB)")
    ax.set_ylabel(f"Decoded Frames (out of {frames})")
    ax.set_title("GRC direct strobe run: SNR vs Decoded Frames")
    ax.grid(True, linestyle="--", alpha=0.45)
    if len(x_values) == 1:
        ax.set_xlim(x_values[0] - 0.5, x_values[0] + 0.5)
    else:
        ax.set_xlim(min(x_values), max(x_values))
    ax.set_ylim(0, frames + 2)
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=180)
    plt.close(fig)


def main():
    args = parse_args()
    grc_source = args.grc.read_text(encoding="utf-8")
    rows = []

    try:
        for snr_db in frange(args.start_snr, args.stop_snr, args.step):
            args.grc.write_text(set_grc_snr(grc_source, snr_db), encoding="utf-8")
            generated_py = generate_flowgraph(args.grc, args.grc.parent)
            row = {
                "snr_db": snr_db,
                **run_generated_flowgraph(
                    generated_py,
                    frames=args.frames,
                    rx_grace=args.rx_grace,
                    max_extra_wait=args.max_extra_wait,
                ),
            }
            rows.append(row)
            write_csv(args.csv, rows)
            write_plot(args.png, rows, args.frames)
            print(
                f"SNR={snr_db:>5.1f} dB -> sent={row['frames_sent']:>3d} "
                f"ok={row['frames_ok']:>3d} "
                f"lost={row['frames_lost']:>3d} bad_crc={row['frames_bad_crc']:>3d} "
                f"time={row['elapsed_s']:.1f}s",
                flush=True,
            )
    finally:
        args.grc.write_text(grc_source, encoding="utf-8")
        generate_flowgraph(args.grc, args.grc.parent)

    print(f"CSV saved to: {args.csv}")
    print(f"Plot saved to: {args.png}")


if __name__ == "__main__":
    main()
