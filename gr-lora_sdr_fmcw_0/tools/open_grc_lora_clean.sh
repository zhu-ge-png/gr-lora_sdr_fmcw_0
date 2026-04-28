#!/usr/bin/env bash
set -euo pipefail

ENV_DIR="/home/lmz/miniconda3/envs/gr310_lora_clean"
FLOWGRAPH="${1:-/home/lmz/gr-lora_sdr_clean/examples/tx_rx_hier_functionality_check.grc}"

export GRC_HIER_PATH="${GRC_HIER_PATH:-/tmp/grc_hier_lora_clean}"
export XDG_CACHE_HOME="${XDG_CACHE_HOME:-/tmp/grc_cache_lora_clean}"
export XDG_CONFIG_HOME="${XDG_CONFIG_HOME:-/tmp/grc_config_lora_clean}"
unset GRC_BLOCKS_PATH
mkdir -p "$GRC_HIER_PATH" "$XDG_CACHE_HOME" "$XDG_CONFIG_HOME"

source /home/lmz/miniconda3/etc/profile.d/conda.sh
conda activate "$ENV_DIR"

exec "$ENV_DIR/bin/gnuradio-companion" --gtk "$FLOWGRAPH"
