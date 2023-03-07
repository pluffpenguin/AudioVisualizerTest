import socket
import time

HOSTNAME = socket.gethostname()
IP_ADDRESS = socket.gethostbyname(HOSTNAME)
PORT = 1234

# create a UDP socket object
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# send a message to the server
message = "Hello, server!"

for i in range(0, 100):
    message = "Message #" + i 
    sock.sendto(message.encode(), (IP_ADDRESS, PORT))
    time.sleep(1)
    
    