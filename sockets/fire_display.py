import socket
import time
import math
import numpy as np
from moduleLedColor import ModuleLed


Strip = ModuleLed()
LED_COUNT = 192

stepMax = math.pi*2
stepTime = max/30.0
step = 0

numSteps = 30
totalTime = 0.5 # seconds
sleepTime = totalTime/numSteps

r = int(input("> Color Input\n Red:"))
g = int(input("Green: "))
b = int(input("Blue:"))

while True:
    mult = np.cos(step)
    Strip.setColor(int(r*mult), int(g*mult), int(b*mult))
    step = step + stepTime
    if step > stepMax:
        step = 0
        
    time.sleep(sleepTime)