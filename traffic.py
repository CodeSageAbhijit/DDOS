#!/usr/bin/env python3

import time
import random
import socket
import sys

host = '192.168.0.113'
port = 8080
message = 'asdf'
conn = int(input("How many connections do you want to make: "))
ip = socket.gethostbyname(host)
n = 0

def generate_traffic():
    global n
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        s.send(f"GET /{message} HTTP/1.1\r\n".encode('utf-8'))
        print("|[Message Sent] |")
    except socket.error as msg:
        n += 1
        print(f"|[Connection Failed] | {n}")
    finally:
        s.close()

while True:
    generate_traffic()
    time.sleep(random.uniform(0.01, 0.025))
