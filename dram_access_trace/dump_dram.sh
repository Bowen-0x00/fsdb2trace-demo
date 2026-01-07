#!/bin/bash

# =========================================================
# Description: Dumps AXI Read Address & Data channels
# Logic: Separates AR and R channels for Python reconstruction
# =========================================================

# Configuration
FSDB_FILE="build_flash/novas.fsdb"

# [USER NOTE]: Update these paths to match your design hierarchy
DRAM_PATH="simtop/path/DDR_SUBSYS"
CLOCK_PATH="simtop/path/clk"

echo "Starting DRAM AXI Dump (Dynamic Burst)..."

# =========================================================
# Loop for Channel 0 and 1
# =========================================================
for i in {0..1}; do
    echo "Processing Channel $i ..."

    # 1. Dump Read Address (AR) Channel + ARLEN
    # We need both Address and Length to calculate beat count
    fsdbreport $FSDB_FILE \
        -exp "(${CLOCK_PATH}==1) && (${DRAM_PATH}/SOC_M_AXI_arvalid[${i}]==1) && (${DRAM_PATH}/SOC_M_AXI_arready[${i}]==1)" \
        -s   "${DRAM_PATH}/SOC_M_AXI_araddr[${i}]" -w 64 -of h \
             "${DRAM_PATH}/SOC_M_AXI_arlen[${i}]" -w 64 -of h \
        -o   "raw_dram_ar_ch${i}.txt" &

    # 2. Dump Read Data (R) Channel
    fsdbreport $FSDB_FILE \
        -exp "(${CLOCK_PATH}==1) && (${DRAM_PATH}/SOC_M_AXI_rvalid[${i}]==1) && (${DRAM_PATH}/SOC_M_AXI_rready[${i}]==1)" \
        -s   "${DRAM_PATH}/SOC_M_AXI_rdata[${i}]" \
        -w 64 -of h \
        -o   "raw_dram_r_ch${i}.txt" &
done

wait
echo "Dump finished."
