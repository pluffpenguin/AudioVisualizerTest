
# Based on NeoPixel library and strandtest example by Tony DiCola (tony@tonydicola.com)
# To be used with a 12x1 NeoPixel LED stripe.
# Place the LEDs in a circle an watch the time go by ...
# red = hours
# blue = minutes 1-5
# green = seconds
# (To run the program permanently and with autostart use systemd.)

from array import array
from random import randint
import time
from time import sleep
import datetime

from rpi_ws281x_python import PixelStrip, Color

# LED strip configuration:
# 6.6 ft LED strip: 192
# rectangle LED strip: 256
# PC Case LED strip: 30cm, 43

# LED_COUNT = 43
# LED_COUNT = int( input("How many LED's?\n>") )        # Number of LED pixels.
LED_COUNT = 192
LED_PIN = 12          # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 50  # Set to 0 for darkest and 255 for brightest
# True to invert the signal (when using NPN transistor level shift)
LED_INVERT = False

SHIFT_TIMER = 0.05

class ModuleLed:
    def __init__(self):
        self.strip = PixelStrip(
        LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
        # Intialize the library (must be called once before other functions).
        self.strip.begin()
        self.strip.show()
        self.currentColor = [0, 0, 0]
        self.targetColor = [0, 0, 0]
    
    def setColor(self, colorArray):
        targetColor = Color(colorArray[0], colorArray[1], colorArray[2])
        for i in range(self.strip.numPixels()-1):
            print('led pin:', i)
            self.strip.setPixelColor(i, targetColor)
        self.strip.show()

    def turnoff(self):
        self.strip.setBrightness(0)
        self.strip.show()