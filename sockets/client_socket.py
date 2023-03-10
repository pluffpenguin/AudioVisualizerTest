import socket

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
HOSTNAME = socket.gethostname()
IP_ADDRESS = socket.gethostbyname(HOSTNAME)
PORT = 1234

ADDR = (IP_ADDRESS, PORT)

client = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
client.connect(ADDR)

print(f"Client Started: {HOSTNAME}, {ADDR}")

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    
send("Hello World!")
    

# print(HOSTNAME, IP_ADDRESS)

# # We need to create UDP Socket communication

# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# # bind the socket to the IP_ADDRESS and PORT
# sock.bind((IP_ADDRESS, PORT))

# # wait for incoming messages
# while True:
#     data, address = sock.recvfrom(1024)  # buffer size is 1024 bytes
#     print(f"Received message: {data.decode()} from {address[0]}:{address[1]}")
