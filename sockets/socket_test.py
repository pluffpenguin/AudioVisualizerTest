import socket
import time

HOSTNAME = socket.gethostname()
# IP_ADDRESS = socket.gethostbyname(HOSTNAME)
# IP_ADDRESS = socket.gethostbyaddr('192.168.1.67')
IP_ADDRESS = "192.168.1.1"
PORT = 1234

print(HOSTNAME, IP_ADDRESS)

# We need to create UDP Socket communication

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# bind the socket to the IP address and port
sock.bind((IP_ADDRESS, PORT))

# wait for incoming messages
while True:
    print(f'Awaiting message...')
    try:
        data, address = sock.recvfrom(1024)  # buffer size is 1024 bytes
        print(f"Received message: {data.decode()} from {address[0]}:{address[1]}")
    except:
        print('> Did not find messgaes...')
        pass
    time.sleep(1)

