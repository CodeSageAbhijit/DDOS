import time
import os
import sys
import string
import threading
import math
from socket import *  # Importing the socket library for network connections

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port

        self.num_connections = 0
        self.num_connects_last_interval = 0
        self.avg_connects_per_interval = 0
        self.num_intervals = -1
        self.ddos_detected = 0

        # Creating socket object
        self.serv = socket(AF_INET, SOCK_STREAM)

        # Bind socket to address
        self.serv.bind((self.host, self.port))
        self.serv.listen(5)  # Setting up the max number of connections we allow as 5
        print('Server up and running! Listening for incoming connections...')

    def collectData(self):
        threading.Timer(3.0, self.collectData).start()  # Collect data every 3 seconds
        self.num_intervals += 1
        if self.num_intervals >= 1:
            print("Num connections in last interval:", self.num_connects_last_interval)
            self.avg_connects_per_interval = ((self.avg_connects_per_interval * (self.num_intervals - 1)) + self.num_connects_last_interval) / self.num_intervals
            print("Avg connections per interval:", self.avg_connects_per_interval)
            errorBound = self.avg_connects_per_interval * self.marginOfError(self.num_intervals, 1.96)  # 95% confidence level
            self.checkBound(errorBound)
        self.num_connects_last_interval = 0

    def marginOfError(self, sampleSize, critValue):
        margin = critValue / (2 * math.sqrt(sampleSize))
        return margin

    def checkBound(self, error):
        if self.num_connects_last_interval > self.avg_connects_per_interval + error and self.ddos_detected == 0:
            print("DDOS WARNING")
            self.ddos_detected = 1
        elif self.num_connects_last_interval > self.avg_connects_per_interval + error and self.ddos_detected > 0:
            print("DDOS DETECTED! ERROR:", self.ddos_detected)
            self.ddos_detected += 1
        elif self.num_connects_last_interval < self.avg_connects_per_interval + error and self.ddos_detected > 1:
            self.ddos_detected = 0
            self.avg_connects_per_interval = 0
            self.num_intervals = -1
        else:
            self.ddos_detected = 0
        print("Error bound:", error)

    def acceptConnections(self):
        while True:
            conn, addr = self.serv.accept()  # Accept incoming connection
            data = conn.recv(1024).decode('utf-8')  # Decode received data to avoid byte issues
            print("Message From " + addr[0] + " : " + data)
            print('Connected by', addr, 'Number of connections:', self.num_connections)
            print(">>>>>>>>>>>>>")
            self.num_connects_last_interval += 1
            self.num_connections += 1
            conn.send('THIS MESSAGE WAS SENT FROM THE SERVER'.encode('utf-8'))  # Encoding message before sending
            conn.close()  # Closing connection after handling

# Setting up variables
HOST = '192.168.0.113'
PORT = 8080

if __name__ == '__main__':
    victimServer = Server(HOST, PORT)

    victimServer.collectData()  # Start data collection in a separate thread

    victimServer.acceptConnections()  # Accept connections continuously
