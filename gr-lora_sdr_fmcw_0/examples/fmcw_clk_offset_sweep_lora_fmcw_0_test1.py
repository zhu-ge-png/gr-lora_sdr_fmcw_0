#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import csv
import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path


THIS_FILE = Path(__file__).resolve()
FLOWGRAPH_PATH = THIS_FILE.with_name("lora_fmcw_0_test1.py")
DEFAULT_CSV = THIS_FILE.with_name("lora_fmcw_0_test1_fmcw_clk_offset_sweep.csv")

RX_RE = re.compile(rb"\[frame_id_tracker rx\] id=(-?\d+|\?) status=(ok|bad)")

os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib")


def parse_int_list(text):
    return [int(part.strip()) for part in text.split(",") if part.strip()]


def parse_float_list(text):
    return [float(part.strip()) for part in text.split(",") if part.strip()]


def format_number(value):
    if float(value).is_integer():
        return str(int(value))
    return f"{value:.6g}"


def make_clk_offset_tag(clk_offset):
    sign = "p" if clk_offset >= 0 else "m"
    magnitude = format_number(abs(clk_offset)).replace(".", "p")
    return f"{sign}{magnitude}"


def parse_args():
    parser = argparse.ArgumentParser(
        description="Sweep mixed FMCW/0-bin preamble split and clk_offset for lora_fmcw_0_test1."
    )
    parser.add_argument("--fmcw-counts", default="1,2,3,4,5,6,8")
    parser.add_argument("--clk-offsets", default="0,1,2,3,4,5,6,8,10")
    parser.add_argument("--frames", type=int, default=50)
    parser.add_argument("--snr", type=float, default=None, help="Override SNRdB; omit to keep flowgraph default.")
    parser.add_argument("--corr-threshold", type=float, default=None)
    parser.add_argument("--idle-timeout", type=float, default=1.5)
    parser.add_argument("--max-wait", type=float, default=8.0)
    parser.add_argument("--poll-interval", type=float, default=0.05)
    parser.add_argument("--post-interval", type=float, default=0.0)
    parser.add_argument("--throttle-rate", type=float, default=200_000_000.0)
    parser.add_argument("--csv", type=Path, default=DEFAULT_CSV)
    parser.add_argument("--run-point", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--fmcw-count", type=int, help=argparse.SUPPRESS)
    parser.add_argument("--clk-offset", type=float, help=argparse.SUPPRESS)
    parser.add_argument("--result-json", type=Path, help=argparse.SUPPRESS)
    return parser.parse_args()


def replace_one(source, pattern, replacement, label):
    updated, count = re.subn(pattern, replacement, source, count=1)
    if count != 1:
        raise RuntimeError(f"Could not override {label} in {FLOWGRAPH_PATH}")
    return updated


def drop_noisy_debug_connections(source):
    noisy_targets = (
        "blocks_message_debug_strobe",
        "blocks_message_debug_radar_up",
        "blocks_message_debug_radar_down",
        "blocks_message_debug_inc",
        "radar_print_results_0",
    )
    kept_lines = []
    for line in source.splitlines():
        if "self.msg_connect" in line and any(target in line for target in noisy_targets):
            continue
        kept_lines.append(line)
    return "\n".join(kept_lines) + "\n"


def load_flowgraph_class(fmcw_count, clk_offset, snr, corr_threshold):
    sys.path.insert(0, str(THIS_FILE.parent))
    source = FLOWGRAPH_PATH.read_text(encoding="utf-8")
    source = replace_one(
        source,
        r"self\.fmcw_triangle_count = fmcw_triangle_count = [-+0-9]+",
        f"self.fmcw_triangle_count = fmcw_triangle_count = {fmcw_count:d}",
        "fmcw_triangle_count",
    )
    source = replace_one(
        source,
        r"self\.clk_offset = clk_offset = [-+0-9.eE]+",
        f"self.clk_offset = clk_offset = {clk_offset:g}",
        "clk_offset",
    )
    if snr is not None:
        source = replace_one(
            source,
            r"self\.SNRdB = SNRdB = [-+0-9.eE]+",
            f"self.SNRdB = SNRdB = {snr:g}",
            "SNRdB",
        )
    if corr_threshold is not None:
        source = replace_one(
            source,
            r"self\.corr_threshold = corr_threshold = [-+0-9.eE]+",
            f"self.corr_threshold = corr_threshold = {corr_threshold:g}",
            "corr_threshold",
        )
    source = drop_noisy_debug_connections(source)

    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        prefix="lora_fmcw_0_test1_fmcw_clk_",
        suffix=".py",
        delete=False,
    ) as handle:
        handle.write(source)
        temp_path = Path(handle.name)

    module_name = f"lora_fmcw_0_test1_fmcw_clk_{os.getpid()}"
    spec = importlib.util.spec_from_file_location(module_name, temp_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    temp_path.unlink(missing_ok=True)
    return module.lora_fmcw_0_test1


def parse_rx_log(log_path, frames):
    data = log_path.read_bytes()
    ok_ids = set()
    bad_crc_ids = []
    rx_total = 0

    for match in RX_RE.finditer(data):
        rx_total += 1
        frame_id_raw, status = match.groups()
        if frame_id_raw == b"?":
            continue
        frame_id = int(frame_id_raw)
        if status == b"ok":
            ok_ids.add(frame_id)
        else:
            bad_crc_ids.append(frame_id)

    expected_ids = set(range(frames))
    frames_ok = len(ok_ids & expected_ids)
    frames_bad_crc = len([frame_id for frame_id in bad_crc_ids if frame_id in expected_ids])
    return {
        "frames_sent": frames,
        "frames_ok": frames_ok,
        "frames_bad_crc": frames_bad_crc,
        "frames_lost": frames - frames_ok,
        "rx_log_count": rx_total,
    }


def write_json(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False)
        handle.flush()
        os.fsync(handle.fileno())


def write_progress(path, message):
    if path is None:
        return
    with path.open("a", encoding="utf-8") as handle:
        handle.write(f"{time.monotonic():.3f} {message}\n")


def run_single_point(args):
    progress_path = args.result_json.with_suffix(".progress") if args.result_json else None
    write_progress(progress_path, "run_single_point_start")
    import pmt
    from gnuradio import blocks
    write_progress(progress_path, "gnuradio_import_done")

    write_progress(progress_path, "load_flowgraph_start")
    flowgraph_cls = load_flowgraph_class(
        args.fmcw_count,
        args.clk_offset,
        args.snr,
        args.corr_threshold,
    )
    write_progress(progress_path, "load_flowgraph_done")

    with tempfile.NamedTemporaryFile(
        prefix=f"fmcw_{args.fmcw_count:02d}_clk_{make_clk_offset_tag(args.clk_offset)}_",
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

        write_progress(progress_path, "construct_tb_start")
        tb = flowgraph_cls()
        write_progress(progress_path, "construct_tb_done")
        tb.blocks_message_strobe_0_0_0.set_period(10_000_000)
        tb.blocks_throttle2_0.set_sample_rate(args.throttle_rate)

        rx_messages = blocks.message_debug()
        tb.msg_connect((tb.lora_sdr_crc_verif_0, "msg"), (rx_messages, "store"))

        write_progress(progress_path, "tb_start")
        tb.start()
        write_progress(progress_path, "post_frames_start")
        for frame_id in range(args.frames):
            tb.lora_sdr_whitening_0_0.to_basic_block()._post(
                pmt.intern("msg"),
                pmt.intern(f"helloworld : {frame_id}"),
            )
            if args.post_interval > 0:
                time.sleep(args.post_interval)
        write_progress(progress_path, "post_frames_done")

        last_progress = start_time
        last_seen = -1
        while True:
            decoded_messages = rx_messages.num_messages()
            if decoded_messages != last_seen:
                last_seen = decoded_messages
                last_progress = time.monotonic()

            now = time.monotonic()
            if decoded_messages >= args.frames:
                break
            if now - start_time >= args.max_wait:
                break
            if now - last_progress >= args.idle_timeout:
                break
            time.sleep(args.poll_interval)
        write_progress(progress_path, f"wait_loop_done decoded={decoded_messages}")

        os.fsync(log_fd)
    finally:
        os.fsync(log_fd)
        os.dup2(saved_stdout_fd, 1)
        os.dup2(saved_stderr_fd, 2)
        os.close(saved_stdout_fd)
        os.close(saved_stderr_fd)
        os.close(log_fd)

    write_progress(progress_path, "parse_log_start")
    stats = parse_rx_log(log_path, args.frames)
    write_progress(progress_path, "parse_log_done")
    log_path.unlink(missing_ok=True)

    result = {
        "fmcw_count": args.fmcw_count,
        "zero_bin_chirps": 8 - args.fmcw_count,
        "clk_offset_ppm": args.clk_offset,
        "snr_db": args.snr,
        "corr_threshold": args.corr_threshold,
        "decoded_messages": decoded_messages,
        "elapsed_s": round(time.monotonic() - start_time, 3),
        **stats,
    }
    write_json(args.result_json, result)
    write_progress(progress_path, "result_written")
    os._exit(0)


def run_point_subprocess(args, fmcw_count, clk_offset):
    with tempfile.NamedTemporaryFile(
        prefix=f"fmcw_{fmcw_count:02d}_clk_{make_clk_offset_tag(clk_offset)}_",
        suffix=".json",
        delete=False,
    ) as handle:
        result_path = Path(handle.name)

    child_code = "\n".join(
        [
            "from argparse import Namespace",
            "from pathlib import Path",
            "import sys",
            f"sys.path.insert(0, {str(THIS_FILE.parent)!r})",
            "import fmcw_clk_offset_sweep_lora_fmcw_0_test1 as sweep",
            "args = Namespace(",
            f"    fmcw_count={fmcw_count!r},",
            f"    clk_offset={clk_offset!r},",
            f"    frames={args.frames!r},",
            f"    snr={args.snr!r},",
            f"    corr_threshold={args.corr_threshold!r},",
            f"    idle_timeout={args.idle_timeout!r},",
            f"    max_wait={args.max_wait!r},",
            f"    poll_interval={args.poll_interval!r},",
            f"    post_interval={args.post_interval!r},",
            f"    throttle_rate={args.throttle_rate!r},",
            f"    result_json=Path({str(result_path)!r}),",
            ")",
            "sweep.run_single_point(args)",
        ]
    )
    cmd = [sys.executable, "-c", child_code]

    progress_path = result_path.with_suffix(".progress")
    try:
        subprocess.run(
            cmd,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=args.max_wait + args.idle_timeout + 10.0,
        )
        with result_path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except subprocess.TimeoutExpired as exc:
        if progress_path.exists():
            print(progress_path.read_text(encoding="utf-8"), file=sys.stderr)
        raise exc
    finally:
        result_path.unlink(missing_ok=True)
        progress_path.unlink(missing_ok=True)


def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "fmcw_count",
        "zero_bin_chirps",
        "clk_offset_ppm",
        "snr_db",
        "corr_threshold",
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


def main():
    args = parse_args()
    fmcw_counts = parse_int_list(args.fmcw_counts)
    clk_offsets = parse_float_list(args.clk_offsets)
    if any(count < 1 or count > 8 for count in fmcw_counts):
        raise SystemExit("Use fmcw counts in [1, 8]; the current radar generator clamps repeat_count to at least 1.")

    rows = []
    for fmcw_count in fmcw_counts:
        for clk_offset in clk_offsets:
            row = run_point_subprocess(args, fmcw_count, clk_offset)
            rows.append(row)
            write_csv(args.csv, rows)
            print(
                f"FMCW={fmcw_count} zero={row['zero_bin_chirps']} "
                f"clk={format_number(clk_offset):>5} ppm -> ok={row['frames_ok']:>3d}/{row['frames_sent']} "
                f"lost={row['frames_lost']:>3d} bad_crc={row['frames_bad_crc']:>3d} "
                f"time={row['elapsed_s']:.2f}s",
                flush=True,
            )

    print(f"CSV saved to: {args.csv}")


if __name__ == "__main__":
    main()
