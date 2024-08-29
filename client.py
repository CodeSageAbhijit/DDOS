from socket import *

# Updated IP address
HOST = '192.168.0.113'
PORT = 8080
ADDR = (HOST, PORT)
BUFSIZE = 2048

client = socket(AF_INET, SOCK_STREAM)
client.connect(ADDR)

# Receive data from the server
data = client.recv(BUFSIZE)
print(data.decode('utf-8'))  # Decode bytes to string

client.close()
