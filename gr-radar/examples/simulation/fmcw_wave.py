import numpy as np
import matplotlib.pyplot as plt
import os

fs = 10_000_000
samp_cw = samp_up = samp_down = 2**14
frame_len = samp_cw + samp_up + samp_down  # 49152

path = "/home/lmz/gr-radar/examples/simulation/fmcw_lora_wave.dat"

print("bytes =", os.path.getsize(path))
f = np.fromfile(path, dtype=np.float32)
print("count =", len(f), "min/max (Hz) =", float(f.min()), float(f.max()))

# 如果你用 Head=49152，这里就正好一帧；否则可以自己截取
N = min(len(f), frame_len)
f = f[:N]
t = np.arange(N) / fs

# 画图时下采样一下，避免线太密看成一块
step = 10
plt.figure(figsize=(14,4))
plt.plot(t[::step]*1e3, (f[::step]/1e6))
plt.xlabel("Time (ms)")
plt.ylabel("Frequency (MHz)")
plt.title("Instantaneous frequency of FMCW chirp (saved from Quadrature Demod)")
plt.grid(True)
plt.tight_layout()
plt.show()

