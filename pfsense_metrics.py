#!/usr/local/bin/python3.11
import subprocess
import json
import ipaddress
import sys
import time

def process_packet(line):
    parts = line.split()
    if len(parts) < 5:
        return None
    try:
        src_ip = parts[2].split(':')[0]
        dst_ip = parts[4].split(':')[0]
        # Validate IP addresses
        ipaddress.ip_address(src_ip)
        ipaddress.ip_address(dst_ip)
    except ValueError:
        return None
    protocol = 'Unknown'
    if 'UDP' in line:
        protocol = 'UDP'
    elif 'TCP' in line:
        protocol = 'TCP'
    elif 'ICMP' in line:
        protocol = 'ICMP'
    return {
        "src_ip": src_ip,
        "dst_ip": dst_ip,
        "protocol": protocol
    }

def continuous_interface_metrics(interface):
    tcpdump_cmd = f"tcpdump -i {interface} -n -l"
    try:
        process = subprocess.Popen(tcpdump_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, universal_newlines=True)
        
        last_time = time.time()
        packet_count = 0
        total_bytes = 0
        
        for line in process.stdout:
            packet = process_packet(line)
            if packet:
                packet_count += 1
                total_bytes += len(line)  # Estimate packet size (not precise, but can be used for rough calculations)
                
                current_time = time.time()
                interval = current_time - last_time
                
                if interval > 0:
                    upload_speed = (total_bytes / interval) / 1024  # Convert to KB/s
                    download_speed = upload_speed  # Simplified; you'd need a more sophisticated approach to differentiate upload and download
                    
                    packet["upload_rate"] = f"{upload_speed:.2f} KB/s"
                    packet["download_rate"] = f"{download_speed:.2f} KB/s"
                    packet["bandwidth"] = f"{(upload_speed + download_speed) / 2:.2f} KB/s"
                    
                    print(json.dumps(packet))
                    sys.stdout.flush()  # Ensure output is sent immediately
                    
                    last_time = current_time
                    total_bytes = 0  # Reset total bytes for the next interval
    except KeyboardInterrupt:
        print("Interrupted by user", file=sys.stderr)
    finally:
        process.terminate()
        process.wait()

if __name__ == "__main__":
    interface = "em1"  # Replace with your interface name
    continuous_interface_metrics(interface)
