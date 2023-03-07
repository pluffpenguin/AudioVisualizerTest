import socket

HOSTNAME = socket.gethostname()
IP_ADDRESS = socket.gethostbyname(HOSTNAME)
PORT = 1234

print(HOSTNAME, IP_ADDRESS)

# We need to create UDP Socket communication

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# bind the socket to the IP_ADDRESS and PORT
sock.bind((IP_ADDRESS, PORT))

# wait for incoming messages
while True:
    data, address = sock.recvfrom(1024)  # buffer size is 1024 bytes
    print(f"Received message: {data.decode()} from {address[0]}:{address[1]}")