import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

fs = 10_000_000
path = "/home/lmz/gr-radar/examples/simulation/fmcw_lora_wave.dat"

# ====== 你必须填对的长度（来自 Tag Debug）======
Nfmcw = 49152             # FMCW: 16384*3
Nlora = 4300800            # <-- 换成你当前 LORA_tags 打印的 frame_len
Ns   = 16384              # LoRa 每个 symbol 的采样点数（你现在目标是=16384）

# LoRa 带宽（只用于设置y轴范围；不影响标注）
BW_lora = 78125.0         # Hz（若你按“1sym=16384点”推出来就是 78125）

# ====== 读文件 ======
x = np.fromfile(path, dtype=np.complex64)
if len(x) < (Nfmcw + Nlora + 2):
    raise SystemExit(f"file too short: samples={len(x)} need >= {Nfmcw+Nlora+2}")

# ====== 只取一个周期：从文件开头取 [FMCW+LoRa] ======
start = 0
period = Nfmcw + Nlora

extra_ms = 0.3                       # “一小点”有多长（毫秒），你自己调
extra = int(extra_ms * 1e-3 * fs)    # 转成采样点

end = start + period + extra
seg = x[start:end]


# ====== 瞬时频率（更稳一点：unwrap 相位再差分）======
phase = np.unwrap(np.angle(seg))
f_inst = np.diff(phase) * fs / (2*np.pi)   # Hz, 长度 = len(seg)-1
t = np.arange(len(f_inst)) / fs * 1e3      # ms

# ====== 生成 FMCW / LoRa 掩码（其它段空白）======
idx = np.arange(len(f_inst))

# 第一个周期 FMCW
mask_fmcw_0 = (idx < (Nfmcw - 1))

# 下一周期 FMCW 的“前 extra 点”（注意 f_inst 比 seg 少1点）
mask_fmcw_1 = (idx >= (period - 1)) & (idx < (period - 1 + extra))

mask_fmcw = mask_fmcw_0 | mask_fmcw_1

# LoRa 只显示第一个周期的 LoRa（下一周期仍然空）
mask_lora = (idx >= (Nfmcw - 1)) & (idx < (period - 1))


f_fmcw = np.where(mask_fmcw, f_inst, np.nan)
f_lora = np.where(mask_lora, f_inst, np.nan)

# ====== LoRa 符号起始点索引（在 f_inst 上的索引）======
# LoRa 在 seg 中从样点 Nfmcw 开始；对应到 f_inst 约从 Nfmcw-1 开始
lora_start_finst = Nfmcw - 1
num_syms = Nlora // Ns   # 一般是整数；若不是整数，你可以用 floor
sym_starts = lora_start_finst + np.arange(num_syms) * Ns

# 每个符号的“起始频率”取该符号开头附近一点（比如第1个差分点）
# 防止边界相位跳变太大，可以取开头后偏移几个点平均
start_offset = 8
avg_len = 16
sym_f0 = []
for s in sym_starts:
    a = int(s + start_offset)
    b = int(min(a + avg_len, len(f_inst)))
    sym_f0.append(np.nanmean(f_inst[a:b]))
sym_f0 = np.array(sym_f0)  # Hz

# ====== 为避免太密：只标每隔 K 个符号一次 ======
K = 1   # 1=每个符号都标；2=每隔1个标；4=每隔3个标...
mark_idx = np.arange(0, len(sym_starts), K)
mark_t = t[sym_starts[mark_idx]]
mark_f = sym_f0[mark_idx]

# ====== 画图：上下两个画布 ======
fig, (ax1, ax2) = plt.subplots(
    2, 1, figsize=(16, 6), sharex=True,
    gridspec_kw={"hspace":0.08}
)

# 上：FMCW（MHz）
ax1.plot(t, f_fmcw/1e6, lw=1.2)
ax1.set_ylabel("FMCW Freq (MHz)")
ax1.set_ylim(-3.2, 3.2)
ax1.grid(True, which="both", alpha=0.3)

# 下：LoRa（kHz）
ax2.plot(t, f_lora/1e3, lw=1.0)
ax2.set_ylabel("LoRa Freq (kHz)")
ax2.set_xlabel("Time (ms)")
ax2.set_ylim(-BW_lora/2/1e3*1.2, BW_lora/2/1e3*1.2)
ax2.grid(True, which="both", alpha=0.3)

# ====== 在 LoRa 子图上标注符号起始频率 ======
ax2.scatter(mark_t, mark_f/1e3, s=18, zorder=3)

# 文本标注：频率值（kHz），避免重叠用小字号 + 只标稀疏点
for tt, ff in zip(mark_t, mark_f):
    ax2.text(tt, ff/1e3, f"{ff/1e3:.1f}k", fontsize=7, va="bottom", ha="left")

# ====== 横轴更细刻度：主刻度 5ms，次刻度 1ms（你可改）======
ax2.xaxis.set_major_locator(MultipleLocator(5))
ax2.xaxis.set_minor_locator(MultipleLocator(1))
ax1.xaxis.set_major_locator(MultipleLocator(5))
ax1.xaxis.set_minor_locator(MultipleLocator(1))
ax1.grid(True, which="minor", alpha=0.12)
ax2.grid(True, which="minor", alpha=0.12)

ax1.set_title("One period: FMCW (top) + LoRa (bottom), mark LoRa symbol start freq")

plt.tight_layout()
plt.show()
