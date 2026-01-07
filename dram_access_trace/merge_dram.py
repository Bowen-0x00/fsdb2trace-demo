import os

# =========================================================
# Configuration
# =========================================================
# Data bus width in bytes. Used to increment address during bursts.
# 64-bit data bus = 8 bytes
BYTES_PER_BEAT = 8 

def parse_ar_log(filename):
    """Parses AR log: Time, Address, ARLen"""
    data_list = []
    if not os.path.exists(filename):
        print(f"Warning: {filename} not found.")
        return data_list

    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('*') or line.startswith('='):
                continue
            
            parts = line.split()
            if len(parts) < 3: continue
                
            try:
                t = float(parts[0])
                addr_val = int(parts[1], 16)
                len_val = int(parts[2], 16)
                data_list.append({'time': t, 'addr': addr_val, 'len': len_val})
            except ValueError:
                continue
    return data_list

def parse_r_log(filename):
    """Parses R log: Time, Data"""
    data_list = []
    if not os.path.exists(filename):
        print(f"Warning: {filename} not found.")
        return data_list

    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('*') or line.startswith('='):
                continue
            
            parts = line.split()
            if len(parts) < 2: continue
                
            try:
                t = float(parts[0])
                d = parts[1]
                data_list.append({'time': t, 'data': d})
            except ValueError:
                continue
    return data_list

def process_channel(ch_id):
    """Matches AR (Addr+Len) with R (Data) using dynamic burst logic."""
    ar_file = f"raw_dram_ar_ch{ch_id}.txt"
    r_file  = f"raw_dram_r_ch{ch_id}.txt"
    
    ar_queue = parse_ar_log(ar_file)
    r_queue  = parse_r_log(r_file)
    
    merged = []
    
    # State Machine Variables
    ar_ptr = 0
    current_base_addr = 0
    beats_remaining = 0
    beat_offset = 0
    
    for r_item in r_queue:
        # Fetch next AR if current burst is done
        if beats_remaining == 0:
            if ar_ptr < len(ar_queue):
                ar_entry = ar_queue[ar_ptr]
                current_base_addr = ar_entry['addr']
                beats_remaining = ar_entry['len'] + 1 # AXI Spec: Burst Len = ARLEN + 1
                beat_offset = 0
                ar_ptr += 1
            else:
                # Error: More data than requests
                current_base_addr = 0
                beats_remaining = 0
                beat_offset = 0

        # Calculate physical address for this beat (Assuming INCR burst)
        current_addr = current_base_addr + (beat_offset * BYTES_PER_BEAT)
        
        merged.append({
            'time': r_item['time'],
            'ch':   ch_id,
            'addr': f"{current_addr:016x}",
            'data': r_item['data']
        })
        
        if beats_remaining > 0:
            beats_remaining -= 1
            beat_offset += 1
            
    return merged

def main():
    print("Starting DRAM trace merge (Dynamic ARLEN)...")
    
    ch0_txns = process_channel(0)
    ch1_txns = process_channel(1)
    
    print(f"Channel 0 transactions: {len(ch0_txns)}")
    print(f"Channel 1 transactions: {len(ch1_txns)}")
    
    all_txns = ch0_txns + ch1_txns
    all_txns.sort(key=lambda x: x['time'])
    
    out_file = "dram_linear_trace.txt"
    try:
        with open(out_file, 'w') as f:
            f.write(f"{'Time':<20} {'CH':<4} {'Address':<18} {'Data (RDATA)':<18}\n")
            f.write("="*65 + "\n")
            for item in all_txns:
                f.write(f"{int(item['time']):<20} {item['ch']:<4} {item['addr']:<18} {item['data']:<18}\n")
        print(f"Done! Merged trace written to {out_file}")
    except IOError as e:
        print(f"Error writing file: {e}")

if __name__ == "__main__":
    main()
