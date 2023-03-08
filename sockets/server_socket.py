import socket
import time

HOSTNAME = socket.gethostname()
# IP_ADDRESS = socket.gethostbyname(HOSTNAME)
IP_ADDRESS = "127.0.1.1"
PORT = 5050

# create a UDP socket object
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# send a message to the server
# message = "Hello, server!"

print(HOSTNAME, IP_ADDRESS)

for i in range(0, 100):
    message = "Message #" + str(i)
    print(f'Sending message: {message}')
    sock.sendto(message.encode(), (IP_ADDRESS, PORT))
    time.sleep(1)
    
    