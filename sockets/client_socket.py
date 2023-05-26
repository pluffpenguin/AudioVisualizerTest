import socket
import time

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
currentColor = [0, 0, 0]
targetColor = [0, 0, 0]

step = [0, 0, 0]
numSteps = 10
stepTime = 1
sleepTime = stepTime/numSteps

def parseColorInfo(new_msg):
    new_msg = new_msg[2:]
    new_msg = new_msg.split(", ")
    for i in range(len(new_msg)):
        new_msg[i] = int(new_msg[i])
    return new_msg

def calculateColorStep():
    step[0] = (targetColor[0] - currentColor[0])/numSteps
    step[1] = (targetColor[1] - currentColor[1])/numSteps
    step[2] = (targetColor[2] - currentColor[2])/numSteps

def calculateNewCurrentColor():
    currentColor[0] = currentColor[0] - step[0]
    currentColor[1] = currentColor[1] - step[1]
    currentColor[2] = currentColor[2] - step[2]

def send(msg):
    global targetColor
    global currentColor
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
        # targetColor = new_msg
        # calculateColorStep()
        # while (currentColor[0] - targetColor[0]) > .1:
        #     calculateNewCurrentColor()
        #     print(currentColor)
        #     sentColor = [int(currentColor[0]), int(currentColor[1]), int(currentColor[2])]
        #     led_strip.setColor(sentColor)
        #     time.sleep(sleepTime)
        # currentColor = targetColor

        
target_input = input()
while target_input != DISCONNECT_MESSAGE:
    send(target_input)

send(DISCONNECT_MESSAGE)
