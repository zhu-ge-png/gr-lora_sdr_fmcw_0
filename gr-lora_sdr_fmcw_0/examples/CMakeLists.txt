# This file is a part of gr-lora_sdr
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

install(
    FILES lora_RX.grc
          lora_TX.grc
          lora_fmcw_0_observe_tf.grc
          lora_fmcw_0_observe_tf.py
          lora_fmcw_0_test1.grc
          lora_fmcw_0_test1.py
          plot_radar_and_mux_timefreq_fixed.py
          run_lora_fmcw_0_test1_radar_timefreq.py
          tx_rx_functionality_check.grc
          tx_rx_hier_functionality_check.grc
          tx_rx_simulation.grc
          tx_rx_usrp.grc
    DESTINATION share/gnuradio/examples/lora_sdr)
