import socket
import sys # needed for exiting

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 12345  # The port used by the server

MESSAGE = b"Hello"

print(f"Targeting host IP: {HOST}")
print(f"Targeting port: {PORT}")
print(f"Sending message: {MESSAGE}")

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP, not SOCK_STREAM this time
s.sendto(MESSAGE, (HOST, PORT))
data, addr = s.recvfrom(1024) # buffer size is 1024 bytes
print(f"Received message: {data}")
sys.exit(0)