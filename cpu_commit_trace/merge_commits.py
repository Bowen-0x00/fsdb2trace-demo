import os

def parse_and_merge(way_count=8):
    """
    Reads raw_commit_X.txt files, parses timestamp/PC/Instr,
    and merges them into a single time-sorted linear trace.
    """
    # List to store all valid commit records
    # Format: {'time': float, 'way': int, 'pc': str, 'instr': str}
    all_commits = []

    print("Start parsing raw files...")

    for way_id in range(way_count):
        filename = f"raw_commit_{way_id}.txt"
        
        if not os.path.exists(filename):
            print(f"Warning: {filename} not found, skipping.")
            continue

        with open(filename, 'r') as f:
            for line_num, line in enumerate(f):
                line = line.strip()
                
                # 1. Skip empty lines and header lines
                if not line or line.startswith('*') or line.startswith('='):
                    continue

                parts = line.split()

                # 2. Ensure line has at least 3 columns (Time, PC, Instr)
                if len(parts) < 3:
                    continue
                
                try:
                    # Parse Timestamp (Column 0)
                    timestamp_str = parts[0]
                    if not timestamp_str[0].isdigit():
                        continue
                        
                    timestamp = float(timestamp_str)
                    
                    # Parse PC (Column 1) and Instr (Column 2)
                    pc = parts[1]
                    instr = parts[2]
                    
                    all_commits.append({
                        'time': timestamp,
                        'way': way_id,
                        'pc': pc,
                        'instr': instr
                    })
                except ValueError:
                    continue

    print(f"Total valid commits found: {len(all_commits)}")
    print("Sorting by Time and Way ID...")

    # Sort Logic: Primary key: Time (asc), Secondary key: Way ID (asc)
    all_commits.sort(key=lambda x: (x['time'], x['way']))

    # Output to file
    output_file = "instr_linear.txt"
    print(f"Writing merged trace to {output_file}...")
    
    with open(output_file, 'w') as f_out:
        # Write Header
        f_out.write(f"{'Time':<20} {'Way':<5} {'PC':<18} {'Instr':<18}\n")
        f_out.write("-" * 65 + "\n")
        
        for item in all_commits:
            line_str = f"{int(item['time']):<20} {item['way']:<5} {item['pc']:<18} {item['instr']:<18}\n"
            f_out.write(line_str)

    print("Done!")

if __name__ == "__main__":
    parse_and_merge()
