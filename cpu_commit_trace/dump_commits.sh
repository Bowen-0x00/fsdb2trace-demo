#!/bin/bash

# =========================================================
# Description: Dumps superscalar commit logs (Ways 0-7)
# Prerequisite: Verdi/fsdbreport must be in PATH
# =========================================================

# Configuration
FSDB_FILE="build_flash/novas.fsdb"

# [USER NOTE]: Update these paths to match your design hierarchy
CORE_PATH="simtop/path/core_with_l2/tile/core/backend/inner_ctrlBlock/rob"
CLOCK_PATH="simtop/path/core_with_l2/tile/core/backend/inner_ctrlBlock/rob/clock"

echo "Starting to dump commit logs for ways 0 to 7..."

# =========================================================
# Batch Dump Loop
# =========================================================
for i in {0..7}; do
    echo "Dumping Way $i ..."
    
    OUT_FILE="raw_commit_${i}.txt"
    
    # Run fsdbreport in the background
    # We use ${i} to dynamically select the signal index
    fsdbreport $FSDB_FILE \
        -exp "(${CLOCK_PATH}==1) && (${CORE_PATH}/io_commits_commitValid_${i}==1) && (${CORE_PATH}/io_commits_isCommit==1)" \
        -s   "${CORE_PATH}/io_commits_info_${i}_debug_pc"    -w 32 -of h \
             "${CORE_PATH}/io_commits_info_${i}_debug_instr" -w 32 -of h \
        -o   "$OUT_FILE" &
        
done

# Wait for all background processes to finish
wait
echo "All dump tasks finished. Ready for Python processing."
