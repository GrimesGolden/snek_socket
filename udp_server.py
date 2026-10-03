import socket

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 12345  # Port to listen on (non-privileged ports are > 1023)
JOKE = b" - [This is a humorous message]"
    
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP, not SOCK_STREAM this time
s.bind((HOST, PORT))

print("Group Two Server Online, waiting for incoming UDP data")
while True:
    data, addr = s.recvfrom(1024) # buffer size is 1024 bytes
    print("received message: %s" % data)
    new_message = data + JOKE
    s.sendto(new_message, addr)
    