import socket
import time
import math
import numpy as np
from moduleLedColor import ModuleLed


Strip = ModuleLed()
LED_COUNT = 192

stepMax = math.pi*2
stepTime = 2*3.14/30.0
step = 0

numSteps = 30
totalTime = 1 # seconds
sleepTime = totalTime/numSteps

r = int(input("> Color Input\n Red:"))
g = int(input("Green: "))
b = int(input("Blue:"))

while True:
    mult = np.cos(step)
    targetColor = [int(r*mult), int(g*mult), int(b*mult)]
    Strip.setColor(targetColor)
    step = step + stepTime
    if step > stepMax:
        step = 0
        
    time.sleep(sleepTime)