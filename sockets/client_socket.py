import socket

from moduleLedColor import ModuleLed

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.5.35"
ADDR = (SERVER, PORT)

print("[CLIENT] Client Started! {ADDR}")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

led_strip = ModuleLed()

def parseColorInfo(new_msg):
    new_msg = new_msg[2:]
    new_msg = new_msg.split(", ")
    for i in range(len(new_msg)):
        new_msg[i] = int(new_msg[i])
    return new_msg

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    new_msg = client.recv(2048).decode(FORMAT)
    print(new_msg)
    if new_msg[0] == 'C':
        new_msg = parseColorInfo(new_msg)
        led_strip.setColor(new_msg)



target_input = input()
while target_input != DISCONNECT_MESSAGE:
    send(target_input)

send(DISCONNECT_MESSAGE)
