#!/usr/bin/env python3
import socket

host = '192.168.0.113'
port = 8080
message = 'asdf'
conn = int(input("How many connections do you want to make: "))  # Ensure conn is an integer
ip = socket.gethostbyname(host)
n = 0

def generate_traffic():
    global n
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        request = f"GET /{message} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
        s.sendall(request.encode('utf-8'))  # Send data in bytes
        print("|[Message Sent] |")
    except socket.error as msg:
        n += 1
        print(f"|[Connection Failed] | {n}")
    finally:
        s.close()

for _ in range(conn):  # Loop for the number of connections specified
    generate_traffic()
