import socket 
import threading
import time
from AudioAnalyzerModel import AudioAnalyzerModel
from audio_module import AudioModule
import pandas as pd
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
AudioAnalyzer = AudioAnalyzerModel(sample_rate = 44100, amp_constant = 6000)

data_csv = pd.read_csv("./data.csv")

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
    # brightness_thread = threading.Thread(target=send_brightness, args=(conn, addr))
    # brightness_thread.start()
    while connected:
        print('[HANDLE_CLIENT] Connected! Starting...')
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"[{addr}] {msg}")
            mood_table = [
                {
                    "mood": "happy",
                    "color": [0, 255, 0]
                },
                {
                    "mood": "sad",
                    "color": [15, 3, 252]
                },
                {
                    "mood": "aggressive",
                    "color": [255, 0, 0]
                },
                {
                    "mood": "chill",
                    "color": [50, 50, 255]
                },
                {
                    "mood": "energetic",
                    "color": [252, 252, 3]
                },
            ]
            try: 
                color = AudioAnalyzer.start(
                    mood_table = mood_table, 
                    training_data = data_csv,
                    training_labels = [i for i in [0, 3, 2, 4, 1] for j in range(48)],
                    recording_length = 2
                    )
                print(f'[KON SERVER] Received Color from AudioAnalyzerModel.start(): {color}')
                send_color(conn, color)
            except:
                print("poops")
        
        print('[HANDLE_CLIENT]: End of While Loop. Restarting...')
                # color = getColorInput()
                # conn.send(f"C:{color[0]}, {color[1]}, {color[2]}".encode(FORMAT))
                # send_color(conn, color)
    conn.close()
        

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    # while True:
    conn, addr = server.accept()
    # color_thread = threading.Thread(target=handle_client, args=(conn, addr))
    # color_thread.start()
    handle_client(conn, addr)
        


print("[STARTING] server is starting...")
start()
