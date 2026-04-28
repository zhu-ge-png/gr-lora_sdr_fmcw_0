# gr-lora_sdr_fmcw_0 + gr-radar FMCW

本仓库包含两个 GNU Radio OOT 模块：

- `gr-lora_sdr_fmcw_0/`：LoRa SDR + FMCW 相关模块和示例。
- `gr-radar/`：FMCW 信号产生相关模块，`gr-lora_sdr_fmcw_0` 中的部分流程图会用到它。

建议先安装 `gr-radar`，再安装 `gr-lora_sdr_fmcw_0`。

## 环境

进入已有 Conda 环境：

```bash
conda activate gr310_fmcw_0
```

如果后续 CMake 没有自动安装到 Conda 环境，可以显式使用：

```bash
-DCMAKE_INSTALL_PREFIX="$CONDA_PREFIX"
```

## 安装 gr-radar

```bash
conda activate gr310_fmcw_0
cd gr-radar
mkdir -p build
cd build
cmake .. -DCMAKE_INSTALL_PREFIX="$CONDA_PREFIX"
make -j"$(nproc)"
make install
```

## 安装 gr-lora_sdr_fmcw_0

```bash
conda activate gr310_fmcw_0
cd gr-lora_sdr_fmcw_0
mkdir -p build
cd build
cmake .. -DCMAKE_INSTALL_PREFIX="$CONDA_PREFIX"
make -j"$(nproc)"
make install
```

## 打开 GNU Radio Companion

安装完成后，设置 GRC blocks 路径并启动 GNU Radio Companion：

```bash
conda activate gr310_fmcw_0
export GRC_BLOCKS_PATH="$CONDA_PREFIX/share/gnuradio/grc/blocks"
gnuradio-companion
```

## 示例

常用 GRC 和 Python 示例在：

- `gr-lora_sdr_fmcw_0/examples/`
- `gr-radar/examples/`

如果修改了 C++ 模块或 GRC block yml 文件，建议重新执行对应模块的 CMake、make 和 make install。

## GitHub 权限说明

GitHub 仓库不能设置单独的访问密码。若只想让部分人看到，建议创建 private 仓库，然后在 GitHub 的 repository settings 中把指定 GitHub 账号加入 collaborators。
