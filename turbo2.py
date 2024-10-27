#!/usr/bin/python3
from scapy.all import *
import threading
import ipaddress
import argparse
import time
import os

BANNER = r""" ________                     __                 
|        \                   |  \                
 \$$$$$$$$__    __   ______  | $$____    ______  
   | $$  |  \  |  \ /      \ | $$    \  /      \ 
   | $$  | $$  | $$|  $$$$$$\| $$$$$$$\|  $$$$$$\
   | $$  | $$  | $$| $$   \$$| $$  | $$| $$  | $$
   | $$  | $$__/ $$| $$      | $$__/ $$| $$__/ $$
   | $$   \$$    $$| $$      | $$    $$ \$$    $$
    \$$    \$$$$$$  \$$       \$$$$$$$   \$$$$$$ 

                 Version: Turbo2

     Source: https://github.com/lilmond/Turbo

"""

def turbo_port_check(hostname: str, port: int, include_port: bool = False, timeout: float = 0.5):
    ip_packet = IP(dst=hostname)

    tcp_packet = TCP(sport=RandShort(), dport=port)
    tcp_packet.options = [('MSS', 1460), ('SAckOK', b''), ('Timestamp', (25699407, 0)), ('NOP', None), ('WScale', 7)]
    
    syn_request = ip_packet / tcp_packet

    results, unans = sr(syn_request, verbose=0, timeout=timeout)

    for result in results:
        try:
            ip = result[1][IP].src
            if result[1][TCP].flags == "SA":
                print(f"{ip}{f':{port}' if include_port else ''}")
        except Exception:
            continue
            
def main():
    print(BANNER)

    if not os.geteuid() == 0:
        print("Please run this script as root.")
        return

    parser = argparse.ArgumentParser(description="Turbo-charged TCP port scanner.")
    parser.add_argument("CIDR", type=str, help="IP CIDR, Example: 10.7.0.0/24")
    parser.add_argument("-p", "--port", type=int, required=True, help="Port to scan.")
    parser.add_argument("-t", "--threads", type=int, default=256, help="Total threads to use for scanning. The more, the faster.")
    parser.add_argument("--timeout", type=float, default=0.5, help="Port check timeout. Default: 0.5")
    parser.add_argument("--include-port", action="store_true", default=False, help="Include port in the output.")

    args = parser.parse_args()

    try:
        network_ips = list(ipaddress.IPv4Network(args.CIDR))
    except Exception:
        print("Error: Invalid IP range.")
        return

    print(f"Scanning {len(network_ips)} ({network_ips[0]} - {network_ips[-1]}) hosts.")
    print(f"Online hosts will be printed below.\n")
    
    for host in network_ips:
        while True:
            if threading.active_count() >= args.threads:
                time.sleep(0.05)
                continue

            break
        
        threading.Thread(target=turbo_port_check, args=[str(host), args.port, args.include_port, args.timeout], daemon=True).start()
    
    while True:
        time.sleep(0.05)
        if threading.active_count() <= 1:
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Ctrl + C break detected. Waiting for the remaining processes to finish.")

        while True:
            time.sleep(0.05)
            if threading.active_count() <= 1:
                break
