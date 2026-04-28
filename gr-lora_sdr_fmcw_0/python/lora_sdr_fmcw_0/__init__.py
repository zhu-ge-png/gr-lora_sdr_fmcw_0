# SPDX-License-Identifier: GPL-3.0-or-later
"""Python package for lora_sdr_fmcw_0"""

try:
    import gnuradio.gr.gr_python
except Exception:
    pass

from .lora_sdr_fmcw_0_python import *

for _name in ("lora_sdr_lora_tx", "lora_sdr_lora_rx"):
    try:
        _mod = __import__(f"{__name__}.{_name}", fromlist=[_name])
        globals()[_name] = getattr(_mod, _name)
    except Exception:
        pass
