#!/usr/bin/sh
export VOLK_GENERIC=1
export GR_DONT_LOAD_PREFS=1
export srcdir=/home/lmz/gr-radar/python/radar
export GR_CONF_CONTROLPORT_ON=False
export PATH="/home/lmz/gr-radar/build_fmcw0_clean/python/radar":"$PATH"
export LD_LIBRARY_PATH="":$LD_LIBRARY_PATH
export PYTHONPATH=/home/lmz/gr-radar/build_fmcw0_clean/test_modules:/home/lmz/gr-radar/build_fmcw0_clean:$PYTHONPATH
/home/lmz/miniconda3/envs/gr310_fmcw_0/bin/python /home/lmz/gr-radar/python/radar/qa_os_cfar_2d_vc.py 
