#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import csv
import os
from collections import defaultdict
from math import ceil
from pathlib import Path


os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib")

THIS_FILE = Path(__file__).resolve()
DEFAULT_CSV = THIS_FILE.with_name("lora_fmcw_0_test1_fmcw_clk_offset_sweep_100frames_step0p5.csv")
DEFAULT_LINE_PNG = THIS_FILE.with_name("lora_fmcw_0_test1_fmcw_clk_offset_vs_decoded_frames_100frames_step0p5.png")
DEFAULT_HEATMAP_PNG = THIS_FILE.with_name("lora_fmcw_0_test1_fmcw_clk_offset_vs_decoded_frames_heatmap_100frames_step0p5.png")
DEFAULT_SUBPLOT_PNG = THIS_FILE.with_name("lora_fmcw_0_test1_fmcw_clk_offset_vs_decoded_frames_subplots_100frames_step0p5.png")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Plot decoded-frame relationships from FMCW count vs clk-offset sweep CSV."
    )
    parser.add_argument("--csv", type=Path, default=DEFAULT_CSV)
    parser.add_argument("--line-png", type=Path, default=DEFAULT_LINE_PNG)
    parser.add_argument("--heatmap-png", type=Path, default=DEFAULT_HEATMAP_PNG)
    parser.add_argument("--subplot-png", type=Path, default=DEFAULT_SUBPLOT_PNG)
    return parser.parse_args()


def load_rows(path):
    with path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    for row in rows:
        row["fmcw_count"] = int(row["fmcw_count"])
        row["clk_offset_ppm"] = float(row["clk_offset_ppm"])
        row["frames_sent"] = int(row["frames_sent"])
        row["frames_ok"] = int(row["frames_ok"])
        row["frames_bad_crc"] = int(row["frames_bad_crc"])
        row["frames_lost"] = int(row["frames_lost"])
    return rows


def write_line_plot(path, rows):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    grouped = defaultdict(list)
    for row in rows:
        grouped[row["fmcw_count"]].append(row)

    frames = rows[0]["frames_sent"] if rows else 0
    fig, ax = plt.subplots(figsize=(10.5, 6.2))

    for fmcw_count in sorted(grouped):
        ordered = sorted(grouped[fmcw_count], key=lambda row: row["clk_offset_ppm"])
        x_values = [row["clk_offset_ppm"] for row in ordered]
        y_values = [row["frames_ok"] for row in ordered]
        ax.plot(
            x_values,
            y_values,
            marker="o",
            linewidth=1.7,
            markersize=3.2,
            label=f"FMCW={fmcw_count}",
        )

    ax.set_xlabel("clk_offset (ppm)")
    ax.set_ylabel(f"Decoded Frames (out of {frames})")
    ax.set_title("lora_fmcw_0_test1: clk_offset vs decoded frames")
    ax.set_xlim(min(row["clk_offset_ppm"] for row in rows), max(row["clk_offset_ppm"] for row in rows))
    ax.set_ylim(0, frames + 2)
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.legend(ncol=2, frameon=True, fontsize=9)
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=180)
    plt.close(fig)


def write_subplot_plot(path, rows):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    grouped = defaultdict(list)
    for row in rows:
        grouped[row["fmcw_count"]].append(row)

    fmcw_counts = sorted(grouped)
    frames = rows[0]["frames_sent"] if rows else 0
    min_clk = min(row["clk_offset_ppm"] for row in rows)
    max_clk = max(row["clk_offset_ppm"] for row in rows)

    cols = 4
    rows_count = ceil(len(fmcw_counts) / cols)
    fig, axes = plt.subplots(rows_count, cols, figsize=(16, 6.8), sharex=True, sharey=True)
    axes = axes.flatten()

    for axis, fmcw_count in zip(axes, fmcw_counts):
        ordered = sorted(grouped[fmcw_count], key=lambda row: row["clk_offset_ppm"])
        x_values = [row["clk_offset_ppm"] for row in ordered]
        y_values = [row["frames_ok"] for row in ordered]
        axis.plot(x_values, y_values, marker="o", linewidth=1.7, markersize=3.0, color="tab:blue")
        axis.set_title(f"FMCW={fmcw_count}")
        axis.set_xlim(min_clk, max_clk)
        axis.set_ylim(0, frames + 2)
        axis.grid(True, linestyle="--", alpha=0.4)

    for axis in axes[len(fmcw_counts):]:
        axis.axis("off")

    for axis in axes[::cols]:
        axis.set_ylabel(f"Decoded Frames\n(out of {frames})")

    for axis in axes[-cols:]:
        if axis.has_data():
            axis.set_xlabel("clk_offset (ppm)")

    fig.suptitle("lora_fmcw_0_test1: clk_offset vs decoded frames by FMCW count", y=1.02)
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def write_heatmap(path, rows):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fmcw_counts = sorted({row["fmcw_count"] for row in rows})
    clk_offsets = sorted({row["clk_offset_ppm"] for row in rows})
    frames = rows[0]["frames_sent"] if rows else 0

    values = []
    for fmcw_count in fmcw_counts:
        value_row = []
        for clk_offset in clk_offsets:
            match = next(
                row["frames_ok"]
                for row in rows
                if row["fmcw_count"] == fmcw_count and row["clk_offset_ppm"] == clk_offset
            )
            value_row.append(match)
        values.append(value_row)

    fig, ax = plt.subplots(figsize=(11, 4.8))
    image = ax.imshow(values, aspect="auto", origin="lower", vmin=0, vmax=frames, cmap="viridis")
    ax.set_xlabel("clk_offset (ppm)")
    ax.set_ylabel("FMCW triangle count")
    ax.set_title("lora_fmcw_0_test1: decoded frames heatmap")
    ax.set_xticks(range(len(clk_offsets)))
    ax.set_xticklabels([f"{value:g}" for value in clk_offsets], rotation=45, ha="right")
    ax.set_yticks(range(len(fmcw_counts)))
    ax.set_yticklabels([str(value) for value in fmcw_counts])

    cbar = fig.colorbar(image, ax=ax)
    cbar.set_label(f"Decoded Frames (out of {frames})")

    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=180)
    plt.close(fig)


def main():
    args = parse_args()
    rows = load_rows(args.csv)
    write_line_plot(args.line_png, rows)
    write_subplot_plot(args.subplot_png, rows)
    write_heatmap(args.heatmap_png, rows)
    print(f"Line plot saved to: {args.line_png}")
    print(f"Subplot figure saved to: {args.subplot_png}")
    print(f"Heatmap saved to: {args.heatmap_png}")


if __name__ == "__main__":
    main()
