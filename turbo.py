#!/usr/bin/python3
from scapy.all import *
import ipaddress
import argparse
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

     Source: https://github.com/lilmond/Turbo

"""

def turbo_port_check(ip_cidr: str, port: int, include_port: bool = False):
    ip_packet = IP(dst=ip_cidr)

    tcp_packet = TCP(sport=RandShort(), dport=port)
    tcp_packet.options = [('MSS', 1460), ('SAckOK', b''), ('Timestamp', (25699407, 0)), ('NOP', None), ('WScale', 7)]
    
    syn_request = ip_packet / tcp_packet

    results, unans = sr(syn_request, verbose=0, timeout=1)

    online_hosts = []

    for result in results:
        try:
            ip = result[1][IP].src
            if result[1][TCP].flags == "SA":
                online_hosts.append(f"{ip}{f':{port}' if include_port else ''}")
        except Exception:
            continue
    
    return online_hosts
            
def main():
    print(BANNER)

    if not os.geteuid() == 0:
        print("Please run this script as root.")
        return

    parser = argparse.ArgumentParser(description="Turbo-charged TCP port scanner.")
    parser.add_argument("CIDR", type=str, help="IP CIDR, Example: 10.7.0.0/24")
    parser.add_argument("-p", "--port", type=int, required=True, help="Port to scan.")
    parser.add_argument("--include-port", action="store_true", default=False, help="Include port in the output.")

    args = parser.parse_args()

    network_ips = list(ipaddress.IPv4Network(args.CIDR))

    print(f"Scanning {len(network_ips)} ({network_ips[0]} - {network_ips[-1]}) hosts.")
    print(f"Online hosts will be printed below.\n")

    online_hosts = turbo_port_check(ip_cidr=args.CIDR, port=args.port, include_port=args.include_port)
    
    for host in online_hosts:
        print(host)
    
    print(f"\nTotal online hosts: {len(online_hosts)}\n")

if __name__ == "__main__":
    main()
