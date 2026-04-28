#!/usr/bin/env bash
set -euo pipefail

ENV_DIR="/home/lmz/miniconda3/envs/gr310_fmcw_0"
FLOWGRAPH="${1:-/home/lmz/gr-lora_sdr_fmcw_0/examples/lora_fmcw_0_test1.grc}"

export GRC_HIER_PATH="${GRC_HIER_PATH:-/tmp/grc_hier_fmcw}"
export XDG_CACHE_HOME="${XDG_CACHE_HOME:-/tmp/grc_cache_fmcw}"
export XDG_CONFIG_HOME="${XDG_CONFIG_HOME:-/tmp/grc_config_fmcw}"
unset GRC_BLOCKS_PATH
mkdir -p "$GRC_HIER_PATH" "$XDG_CACHE_HOME" "$XDG_CONFIG_HOME"

source /home/lmz/miniconda3/etc/profile.d/conda.sh
conda activate "$ENV_DIR"

exec "$ENV_DIR/bin/gnuradio-companion" --gtk "$FLOWGRAPH"
