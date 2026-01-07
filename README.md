# FSDB Trace Toolkit

**fsdb-trace-toolkit** is a collection of scripts designed to bridge the gap between waveform debugging (FSDB) and data analysis. It extracts signal activities from FSDB files and processes them into human-readable, linear text traces.

[Read in Chinese (中文版)](README_zh.md)

> [!IMPORTANT]
> **Performance Note**
>
> This project is designed for demonstration and prototyping purposes.
> * **Current Implementation**: Uses shell scripts (calling `fsdbreport`) and Python for text parsing.
> * **Limitations**: May have high I/O overhead for very large waveforms (GB/TB scale).
> * **Optimizations**: For production, consider using Synopsys API or logging directly from simulation.

---

## 🚀 Features

- **Superscalar Commit Trace**: Converts multi-way ROB commit signals into a single, time-ordered instruction execution stream.
- **DRAM Access Trace**: Reconstructs AXI read transactions by matching Address (AR) and Data (R) channels.

## 🛠 Prerequisites

- **Verdi / fsdbreport**: Must be installed and accessible in your `$PATH`.
- **Python 3.x**: Standard library only.
- **Bash**: For running extraction scripts.

## 📂 Structure

```text
fsdb-trace-toolkit/
├── cpu_commit_trace/         # Demo 1: Superscalar CPU Commits
│   ├── dump_commits.sh       # Bash: Export data via fsdbreport
│   └── merge_commits.py      # Python: Merge into linear trace
└── dram_access_trace/        # Demo 2: DRAM Access Sequence
    ├── dump_dram.sh          # Bash: Export AR and R channels
    └── merge_dram.py         # Python: Handle burst logic and merge
```

## 📖 Usage

### Step 1: Configure Paths
Update the variables in the `.sh` scripts:
- `FSDB_FILE`: Path to your waveform.
- `CORE_PATH` / `DRAM_PATH`: RTL hierarchy paths.
- `CLOCK_PATH`: Sampling clock.

### Step 2: Run Extraction & Processing

**CPU Commit Trace:**
```bash
cd cpu_commit_trace
chmod +x dump_commits.sh
./dump_commits.sh
python3 merge_commits.py
```

**DRAM Access Trace:**
```bash
cd dram_access_trace
chmod +x dump_dram.sh
./dump_dram.sh
python3 merge_dram.py
```

## 📄 License
MIT License
