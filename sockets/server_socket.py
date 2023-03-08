import socket
import threading
import time

HEADER = 64
HOSTNAME = socket.gethostname()
# IP_ADDRESS = socket.gethostbyname(HOSTNAME)
IP_ADDRESS = "127.0.1.1"
PORT = 5050
ADDR = (IP_ADDRESS, PORT)
FORMAT = 'utf-8'

# create a UDP socket object
# AF_INET6 is meant for IPv6 Addresses

# https://www.youtube.com/watch?v=3QiPPX-KeSc&t=1229s
server = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
server.bind(ADDR)

# send a message to the server
# message = "Hello, server!"

print(f"{HOSTNAME}, {IP_ADDRESS}")

def handle_client(conn, addr):
    print(f"[NEW CONNECTION]: {addr} connected.")
    connected = True
    while connected:
        # Blocking Line: We will not pass until we receive data
        # HEADER = 64 bytes. It is fixed into this length
        # Every message is encoded in byte format. We need to decode it
        msg_length = conn.recv(HEADER).decode(FORMAT)
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(FORMAT)
        print(f"[{addr}]: {msg}")
        # Handle clean disconnections.
        # If clients do not tell the server, 
        # Then it thinks they're still connected upon reconnection
        
        
        

def start():
    server.listen()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount()-1}")
        

# for i in range(0, 100):
#     message = "Message #" + str(i)
#     print(f'Sending message: {message}')
#     server.sendto(message.encode(), (IP_ADDRESS, PORT))
#     time.sleep(1)
    
    