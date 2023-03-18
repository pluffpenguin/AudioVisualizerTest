import socket 
import threading
import time
from AudioAnalyzerModel import AudioAnalyzerModel
from audio_module import AudioModule

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

print(f"[PRINT] Address: {ADDR}")

audioMod = AudioModule(50)

def getColorInput():
    print('Input the RGB Values, separated by a space:')
    color = input()
    color = color.split(' ')
    return color

def send_brightness(conn, addr):
    while True:
        brightness_message = f"B:{audioMod.getBrightnessInt()}"
        conn.send(brightness_message.encode(FORMAT))

def send_color(conn, color):
    conn.send(f"C:{color[0]}, {color[1]}, {color[2]}".encode(FORMAT))

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"[{addr}] {msg}")
            
            color = AudioAnalyzerModel.start()
            print(f'[KON SERVER] Received Color from AudioAnalyzerModel.start(): {color}')
            send_color(conn, color)
                # color = getColorInput()
                # conn.send(f"C:{color[0]}, {color[1]}, {color[2]}".encode(FORMAT))
                # send_color(conn, color)
                
                # brightness_thread = threading.Thread(target=send_brightness, args=(conn, addr))
                # brightness_thread.start()
            
    conn.close()
        

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    #while True:
    conn, addr = server.accept()
    color_thread = threading.Thread(target=handle_client, args=(conn, addr))
    color_thread.start()
    
    print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
        


print("[STARTING] server is starting...")
start()
