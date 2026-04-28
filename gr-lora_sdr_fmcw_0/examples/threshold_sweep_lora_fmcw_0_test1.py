#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import csv
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


THIS_FILE = Path(__file__).resolve()
SNR_SWEEP = THIS_FILE.with_name("snr_sweep_lora_fmcw_0_test1.py")
DEFAULT_DETAIL_CSV = THIS_FILE.with_name("lora_fmcw_0_test1_threshold_sweep_detail.csv")
DEFAULT_SUMMARY_CSV = THIS_FILE.with_name("lora_fmcw_0_test1_threshold_sweep_summary.csv")
DEFAULT_SUMMARY_PNG = THIS_FILE.with_name("lora_fmcw_0_test1_threshold_sweep_summary.png")
DEFAULT_BEST_CSV = THIS_FILE.with_name("lora_fmcw_0_test1_best_threshold_snr_sweep.csv")
DEFAULT_BEST_PNG = THIS_FILE.with_name("lora_fmcw_0_test1_best_threshold_snr_sweep.png")

os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Find the best corr_threshold over an SNR sweep."
    )
    parser.add_argument("--threshold-start", type=float, default=0.22)
    parser.add_argument("--threshold-stop", type=float, default=0.27)
    parser.add_argument("--threshold-step", type=float, default=0.01)
    parser.add_argument(
        "--thresholds",
        default=None,
        help="Comma-separated threshold list. Overrides start/stop/step.",
    )
    parser.add_argument("--start-snr", type=float, default=-10.0)
    parser.add_argument("--stop-snr", type=float, default=10.0)
    parser.add_argument("--snr-step", type=float, default=0.5)
    parser.add_argument("--frames", type=int, default=100)
    parser.add_argument("--idle-timeout", type=float, default=1.5)
    parser.add_argument("--max-wait", type=float, default=10.0)
    parser.add_argument("--detail-csv", type=Path, default=DEFAULT_DETAIL_CSV)
    parser.add_argument("--summary-csv", type=Path, default=DEFAULT_SUMMARY_CSV)
    parser.add_argument("--summary-png", type=Path, default=DEFAULT_SUMMARY_PNG)
    parser.add_argument("--best-csv", type=Path, default=DEFAULT_BEST_CSV)
    parser.add_argument("--best-png", type=Path, default=DEFAULT_BEST_PNG)
    return parser.parse_args()


def frange(start, stop, step):
    values = []
    idx = 0
    while True:
        value = round(start + idx * step, 10)
        if value > stop + 1e-9:
            break
        values.append(value)
        idx += 1
    return values


def parse_thresholds(args):
    if args.thresholds:
        return [float(value.strip()) for value in args.thresholds.split(",") if value.strip()]
    return frange(args.threshold_start, args.threshold_stop, args.threshold_step)


def run_threshold(args, threshold):
    with tempfile.NamedTemporaryFile(prefix=f"thr_{threshold:.3f}_", suffix=".csv", delete=False) as csv_file:
        csv_path = Path(csv_file.name)
    with tempfile.NamedTemporaryFile(prefix=f"thr_{threshold:.3f}_", suffix=".png", delete=False) as png_file:
        png_path = Path(png_file.name)

    cmd = [
        sys.executable,
        str(SNR_SWEEP),
        "--start-snr",
        str(args.start_snr),
        "--stop-snr",
        str(args.stop_snr),
        "--step",
        str(args.snr_step),
        "--frames",
        str(args.frames),
        "--idle-timeout",
        str(args.idle_timeout),
        "--max-wait",
        str(args.max_wait),
        "--corr-threshold",
        str(threshold),
        "--csv",
        str(csv_path),
        "--png",
        str(png_path),
    ]

    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )
    for line in proc.stdout:
        print(f"[thr={threshold:.3f}] {line}", end="", flush=True)
    ret = proc.wait()
    if ret != 0:
        raise subprocess.CalledProcessError(ret, cmd)

    rows = list(csv.DictReader(csv_path.open("r", encoding="utf-8")))
    return csv_path, png_path, rows


def write_detail(path, threshold_rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "corr_threshold",
        "snr_db",
        "frames_sent",
        "frames_ok",
        "frames_bad_crc",
        "frames_lost",
        "decoded_messages",
        "rx_log_count",
        "elapsed_s",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for rows in threshold_rows.values():
            for row in rows:
                writer.writerow({key: row[key] for key in fieldnames})


def summarize(threshold_rows):
    summary = []
    for threshold, rows in threshold_rows.items():
        losses = [int(row["frames_lost"]) for row in rows]
        bad_crc = [int(row["frames_bad_crc"]) for row in rows]
        summary.append(
            {
                "corr_threshold": threshold,
                "total_lost": sum(losses),
                "avg_lost": sum(losses) / len(losses),
                "max_lost": max(losses),
                "zero_loss_points": sum(1 for loss in losses if loss == 0),
                "total_bad_crc": sum(bad_crc),
            }
        )
    summary.sort(key=lambda row: (row["total_lost"], row["max_lost"], -row["zero_loss_points"]))
    return summary


def write_summary(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "corr_threshold",
        "total_lost",
        "avg_lost",
        "max_lost",
        "zero_loss_points",
        "total_bad_crc",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_summary_plot(path, rows):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    ordered = sorted(rows, key=lambda row: row["corr_threshold"])
    thresholds = [row["corr_threshold"] for row in ordered]
    losses = [row["total_lost"] for row in ordered]

    fig, ax = plt.subplots(figsize=(8, 4.8))
    ax.plot(thresholds, losses, marker="o", linewidth=1.8)
    ax.set_xlabel("corr_threshold")
    ax.set_ylabel("Total Lost Frames across SNR sweep")
    ax.set_title("Threshold Search: Total Lost Frames")
    ax.grid(True, linestyle="--", alpha=0.45)
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=180)
    plt.close(fig)


def main():
    args = parse_args()
    thresholds = parse_thresholds(args)
    threshold_rows = {}
    artifacts = {}

    for threshold in thresholds:
        csv_path, png_path, rows = run_threshold(args, threshold)
        threshold_rows[threshold] = rows
        artifacts[threshold] = (csv_path, png_path)
        total_lost = sum(int(row["frames_lost"]) for row in rows)
        print(f"[thr={threshold:.3f}] total_lost={total_lost}", flush=True)

    summary = summarize(threshold_rows)
    best = summary[0]
    best_threshold = best["corr_threshold"]
    best_csv, best_png = artifacts[best_threshold]

    write_detail(args.detail_csv, threshold_rows)
    write_summary(args.summary_csv, summary)
    write_summary_plot(args.summary_png, summary)
    shutil.copyfile(best_csv, args.best_csv)
    shutil.copyfile(best_png, args.best_png)

    for csv_path, png_path in artifacts.values():
        csv_path.unlink(missing_ok=True)
        png_path.unlink(missing_ok=True)

    print(
        f"Best corr_threshold={best_threshold:.3f}, "
        f"total_lost={best['total_lost']}, avg_lost={best['avg_lost']:.2f}, "
        f"max_lost={best['max_lost']}"
    )
    print(f"Summary CSV saved to: {args.summary_csv}")
    print(f"Detail CSV saved to: {args.detail_csv}")
    print(f"Summary plot saved to: {args.summary_png}")
    print(f"Best SNR CSV saved to: {args.best_csv}")
    print(f"Best SNR plot saved to: {args.best_png}")


if __name__ == "__main__":
    main()
