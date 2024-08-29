#!/usr/bin/env python3

import random
import time
from scapy.all import *

HOST = '192.168.0.113'  # Updated IP address
PORT = 8080

while True:
    source = ".".join(map(str, (random.randint(0, 255) for _ in range(4))))
    packet = IP(src=source, dst=HOST) / TCP(dport=PORT) / "HELLO"
    send(packet)
    print(f"Sent packet to: {HOST} From Source IP: {source}")
    time.sleep(random.uniform(0, 2))
