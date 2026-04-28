#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import csv
import importlib.util
import json
import math
import os
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path


THIS_FILE = Path(__file__).resolve()
DEFAULT_CSV = THIS_FILE.with_name("lora_fmcw_0_test1_snr_sweep.csv")
DEFAULT_PNG = THIS_FILE.with_name("lora_fmcw_0_test1_snr_sweep.png")
RX_RE = re.compile(rb"\[frame_id_tracker rx\] id=(-?\d+|\?) status=(ok|bad)")
TX_RE = re.compile(rb"\[frame_id_tracker tx\] id=(-?\d+|\?)")

os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Sweep SNR for the current lora_fmcw_0_test1 flowgraph."
    )
    parser.add_argument("--start-snr", type=float, default=-10.0)
    parser.add_argument("--stop-snr", type=float, default=10.0)
    parser.add_argument("--step", type=float, default=0.5)
    parser.add_argument("--frames", type=int, default=100)
    parser.add_argument(
        "--warmup-frames",
        type=int,
        default=0,
        help="Ignore this many initial strobe-transmitted frames before counting results.",
    )
    parser.add_argument("--idle-timeout", type=float, default=1.5)
    parser.add_argument("--max-wait", type=float, default=10.0)
    parser.add_argument("--poll-interval", type=float, default=0.05)
    parser.add_argument("--post-interval", type=float, default=0.0)
    parser.add_argument(
        "--use-strobe",
        action="store_true",
        help="Use the flowgraph message strobe pacing instead of fast manual posting.",
    )
    parser.add_argument(
        "--strobe-period-ms",
        type=int,
        default=None,
        help="Override the flowgraph message strobe period when --use-strobe is set.",
    )
    parser.add_argument("--corr-threshold", type=float, default=None)
    parser.add_argument(
        "--plot-metric",
        choices=["frames_lost", "frames_ok", "frames_bad_crc", "decoded_messages"],
        default="frames_lost",
        help="Metric to draw on the y-axis.",
    )
    parser.add_argument(
        "--throttle-rate",
        type=float,
        default=200_000_000.0,
        help="Throttle rate used only to speed up this offline experiment.",
    )
    parser.add_argument("--csv", type=Path, default=DEFAULT_CSV)
    parser.add_argument("--png", type=Path, default=DEFAULT_PNG)
    parser.add_argument("--run-point", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--snr", type=float, help=argparse.SUPPRESS)
    parser.add_argument("--result-json", type=Path, help=argparse.SUPPRESS)
    return parser.parse_args()


def frange(start, stop, step):
    if step <= 0:
        raise ValueError("step must be positive")

    count = int(round((stop - start) / step))
    if not math.isclose(start + count * step, stop, abs_tol=1e-9):
        raise ValueError("stop must align with start and step")

    return [round(start + idx * step, 10) for idx in range(count + 1)]


def write_json(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False)
        handle.flush()
        os.fsync(handle.fileno())


def load_flowgraph_class(corr_threshold):
    sys.path.insert(0, str(THIS_FILE.parent))

    if corr_threshold is None:
        from lora_fmcw_0_test1 import lora_fmcw_0_test1

        return lora_fmcw_0_test1

    flowgraph_path = THIS_FILE.with_name("lora_fmcw_0_test1.py")
    source = flowgraph_path.read_text(encoding="utf-8")
    source, count = re.subn(
        r"self\.corr_threshold = corr_threshold = [-+0-9.eE]+",
        f"self.corr_threshold = corr_threshold = {corr_threshold!r}",
        source,
        count=1,
    )
    if count != 1:
        raise RuntimeError("Could not override corr_threshold in lora_fmcw_0_test1.py")

    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        prefix="lora_fmcw_0_test1_threshold_",
        suffix=".py",
        delete=False,
    ) as handle:
        handle.write(source)
        temp_path = Path(handle.name)

    module_name = f"lora_fmcw_0_test1_threshold_{os.getpid()}"
    spec = importlib.util.spec_from_file_location(module_name, temp_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    temp_path.unlink(missing_ok=True)
    return module.lora_fmcw_0_test1


def parse_rx_log(log_path, frames, warmup_frames=0):
    data = log_path.read_bytes()
    tx_ids = []
    ok_ids = set()
    bad_crc_total = 0
    rx_total = 0

    for match in TX_RE.finditer(data):
        frame_id_raw = match.group(1)
        if frame_id_raw != b"?":
            tx_ids.append(int(frame_id_raw))

    for match in RX_RE.finditer(data):
        rx_total += 1
        frame_id_raw, status = match.groups()
        if status == b"ok" and frame_id_raw != b"?":
            frame_id = int(frame_id_raw)
            if frame_id >= 0:
                ok_ids.add(frame_id)
        else:
            bad_crc_total += 1

    if tx_ids:
        expected_ids = set(tx_ids[warmup_frames : warmup_frames + frames])
        ok_ids = ok_ids & expected_ids
        frames_sent = len(expected_ids)
    else:
        expected_ids = set(range(frames))
        frames_sent = frames

    return {
        "frames_sent": frames_sent,
        "frames_ok": len(ok_ids),
        "frames_bad_crc": bad_crc_total,
        "frames_lost": frames_sent - len(ok_ids),
        "rx_log_count": rx_total,
        "ok_ids": sorted(ok_ids),
        "tx_ids": tx_ids[:frames],
    }


def count_tx_ids(log_path):
    data = log_path.read_bytes()
    count = 0
    for match in TX_RE.finditer(data):
        if match.group(1) != b"?":
            count += 1
    return count


def run_single_point(args):
    import pmt
    from gnuradio import blocks

    lora_fmcw_0_test1 = load_flowgraph_class(args.corr_threshold)

    with tempfile.NamedTemporaryFile(
        prefix=f"snr_point_{args.snr:+05.1f}_",
        suffix=".log",
        delete=False,
    ) as handle:
        log_path = Path(handle.name)

    saved_stdout_fd = os.dup(1)
    saved_stderr_fd = os.dup(2)
    log_fd = os.open(log_path, os.O_WRONLY | os.O_APPEND)

    start_time = time.monotonic()
    decoded_messages = 0

    try:
        os.dup2(log_fd, 1)
        os.dup2(log_fd, 2)

        tb = lora_fmcw_0_test1()
        if args.use_strobe:
            if args.strobe_period_ms is not None:
                tb.blocks_message_strobe_0_0_0.set_period(args.strobe_period_ms)
        else:
            tb.blocks_message_strobe_0_0_0.set_period(10_000_000)
        tb.blocks_throttle2_0.set_sample_rate(args.throttle_rate)
        tb.set_SNRdB(args.snr)

        rx_messages = blocks.message_debug()
        tb.msg_connect((tb.lora_sdr_crc_verif_0, "msg"), (rx_messages, "store"))

        tb.start()
        if args.use_strobe:
            while True:
                now = time.monotonic()
                if count_tx_ids(log_path) >= args.warmup_frames + args.frames:
                    last_progress = now
                    break
                if now - start_time >= args.max_wait:
                    break
                time.sleep(args.poll_interval)
        else:
            for frame_id in range(args.frames):
                tb.lora_sdr_whitening_0_0.to_basic_block()._post(
                    pmt.intern("msg"),
                    pmt.intern(f"helloworld : {frame_id}"),
                )
                if args.post_interval > 0:
                    time.sleep(args.post_interval)

        last_progress = start_time
        last_seen = -1
        while True:
            decoded_messages = rx_messages.num_messages()
            if decoded_messages != last_seen:
                last_seen = decoded_messages
                last_progress = time.monotonic()

            now = time.monotonic()
            target_decoded = args.frames + (args.warmup_frames if args.use_strobe else 0)
            if decoded_messages >= target_decoded:
                break
            if now - start_time >= args.max_wait:
                break
            if now - last_progress >= args.idle_timeout:
                break

            time.sleep(args.poll_interval)

        tb.stop()
        time.sleep(0.1)
    finally:
        os.fsync(log_fd)
        os.dup2(saved_stdout_fd, 1)
        os.dup2(saved_stderr_fd, 2)
        os.close(saved_stdout_fd)
        os.close(saved_stderr_fd)
        os.close(log_fd)

    stats = parse_rx_log(log_path, args.frames, args.warmup_frames if args.use_strobe else 0)
    log_path.unlink(missing_ok=True)

    result = {
        "snr_db": args.snr,
        "corr_threshold": args.corr_threshold,
        "decoded_messages": decoded_messages,
        "elapsed_s": round(time.monotonic() - start_time, 3),
        **stats,
    }
    write_json(args.result_json, result)
    os._exit(0)


def run_point_subprocess(args, snr_db):
    with tempfile.NamedTemporaryFile(
        prefix=f"snr_{snr_db:+05.1f}_",
        suffix=".json",
        delete=False,
    ) as handle:
        result_path = Path(handle.name)

    cmd = [
        sys.executable,
        str(THIS_FILE),
        "--run-point",
        "--snr",
        str(snr_db),
        "--frames",
        str(args.frames),
        "--warmup-frames",
        str(args.warmup_frames),
        "--idle-timeout",
        str(args.idle_timeout),
        "--max-wait",
        str(args.max_wait),
        "--poll-interval",
        str(args.poll_interval),
        "--post-interval",
        str(args.post_interval),
        "--throttle-rate",
        str(args.throttle_rate),
        "--result-json",
        str(result_path),
    ]
    if args.use_strobe:
        cmd.append("--use-strobe")
        if args.strobe_period_ms is not None:
            cmd.extend(["--strobe-period-ms", str(args.strobe_period_ms)])
    if args.corr_threshold is not None:
        cmd.extend(["--corr-threshold", str(args.corr_threshold)])

    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        with result_path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    finally:
        result_path.unlink(missing_ok=True)


def write_csv(path, rows):
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
        for row in rows:
            writer.writerow({key: row[key] for key in fieldnames})


def write_plot(path, rows, frames, metric):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    x_values = [row["snr_db"] for row in rows]
    y_values = [row[metric] for row in rows]
    labels = {
        "frames_lost": f"Lost Frames (out of {frames})",
        "frames_ok": f"Decoded Frames (out of {frames})",
        "frames_bad_crc": f"Bad CRC Frames (out of {frames})",
        "decoded_messages": "Decoded Messages",
    }
    titles = {
        "frames_lost": "Current lora_fmcw_0_test1: SNR vs Lost Frames",
        "frames_ok": "Current lora_fmcw_0_test1: SNR vs Decoded Frames",
        "frames_bad_crc": "Current lora_fmcw_0_test1: SNR vs Bad CRC Frames",
        "decoded_messages": "Current lora_fmcw_0_test1: SNR vs Decoded Messages",
    }

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(x_values, y_values, marker="o", linewidth=1.8, markersize=3.5)
    ax.set_xlabel("SNR (dB)")
    ax.set_ylabel(labels[metric])
    ax.set_title(titles[metric])
    ax.grid(True, linestyle="--", alpha=0.45)
    if len(x_values) == 1:
        ax.set_xlim(x_values[0] - 0.5, x_values[0] + 0.5)
    else:
        ax.set_xlim(min(x_values), max(x_values))
    ax.set_ylim(bottom=0)
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=180)
    plt.close(fig)


def main():
    args = parse_args()

    if args.run_point:
        if args.snr is None or args.result_json is None:
            raise SystemExit("--run-point requires --snr and --result-json")
        run_single_point(args)
        return

    rows = []
    for snr_db in frange(args.start_snr, args.stop_snr, args.step):
        row = run_point_subprocess(args, snr_db)
        rows.append(row)
        print(
            f"SNR={snr_db:>5.1f} dB -> lost={row['frames_lost']:>3d} "
            f"ok={row['frames_ok']:>3d} bad_crc={row['frames_bad_crc']:>3d} "
            f"time={row['elapsed_s']:.2f}s",
            flush=True,
        )

    write_csv(args.csv, rows)
    write_plot(args.png, rows, args.frames, args.plot_metric)

    print(f"CSV saved to: {args.csv}")
    print(f"Plot saved to: {args.png}")


if __name__ == "__main__":
    main()
