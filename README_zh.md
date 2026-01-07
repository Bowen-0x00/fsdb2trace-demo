# FSDB Trace Toolkit (中文版)

**fsdb-trace-toolkit** 是一套用于演示如何从 Synopsys FSDB 波形中提取并处理线性轨迹（Linear Trace）的工具集。它包含用于提取 CPU 指令提交序列和 DRAM 访存序列的 Demo 脚本。

[English Version (英文版)](README.md)

> [!IMPORTANT]
> **性能说明 (Performance Note)**
> 
> 本项目旨在演示 **FSDB -> Text -> Trace** 的处理逻辑与原型验证。
> *   **当前实现**：采用了较为直观的 Shell 脚本（调用 `fsdbreport`）配合 Python 文本解析的方式。
> *   **局限性**：这种方式涉及大量的磁盘 I/O 和进程开销。对于 GB/TB 级别的超大波形或生产环境的自动化回归，当前的性能可能不够理想。
> *   **优化方向**：在生产环境中，建议通过优化 `fsdbreport` 过滤表达式、使用 Synopsys API 直接读取二进制数据，或在仿真阶段直接打印 Log 来获得更高的效率。

---

## 🚀 功能演示 (Features)

- **Superscalar Commit Trace**: 将多路（Way 0-7）ROB 提交信号转换为单一时间序的指令流。
- **DRAM Access Trace**: 重组 AXI 总线的读地址（AR）和读数据（R）通道，支持动态 Burst 长度计算。

## 🛠 前置要求 (Prerequisites)

- **Verdi / fsdbreport**: 必须安装并配置在系统 `$PATH` 中。
- **Python 3.x**: 仅需标准库。
- **Bash**: 用于运行提取脚本。

## 📂 目录结构 (Structure)

```text
fsdb-trace-toolkit/
├── cpu_commit_trace/         # Demo 1: 超标量处理器指令提交
│   ├── dump_commits.sh       # Bash: 调用 fsdbreport 导出数据
│   └── merge_commits.py      # Python: 合并多路数据为线性 Trace
└── dram_access_trace/        # Demo 2: DDR 读访问序列
    ├── dump_dram.sh          # Bash: 导出 AR 和 R 通道数据
    └── merge_dram.py         # Python: 处理 Burst 逻辑并合并通道
```

## 📖 使用方法 (Usage)

### Step 1: 配置路径
打开对应目录下的 `.sh` 脚本，修改以下变量以匹配你的设计层次：
- `FSDB_FILE`: `.fsdb` 波形文件路径。
- `CORE_PATH` / `DRAM_PATH`: 模块实例路径。
- `CLOCK_PATH`: 用于采样的时钟信号路径。

### Step 2: 运行提取与处理

**Demo 1: CPU Commit Trace**
```bash
cd cpu_commit_trace
chmod +x dump_commits.sh
./dump_commits.sh      # 导出原始数据
python3 merge_commits.py # 合并并生成 instr_linear.txt
```

**Demo 2: DRAM Access Trace**
```bash
cd dram_access_trace
chmod +x dump_dram.sh
./dump_dram.sh         # 导出原始数据
python3 merge_dram.py    # 处理 Burst 并生成 dram_linear_trace.txt
```

## 📄 License
MIT License
