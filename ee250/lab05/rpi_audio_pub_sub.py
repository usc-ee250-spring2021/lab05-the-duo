"""EE 250L Lab 04 Starter Code
Jeffrey Liu
Aaron Sesay
https://github.com/usc-ee250-spring2021/lab05-the-duo.git
Run rpi_pub_and_sub.py on your Raspberry Pi."""

import paho.mqtt.client as mqtt
import time
#import PWM
#import grovepi
#import grove_rgb_lcd
#from grove_rgb_lcd import *


# GrovePi + Grove Buzzer
import time
import grovepi

# Connect the Grove Buzzer to digital port D8
# SIG,NC,VCC,GND
buzzer = 8

grovepi.pinMode(buzzer,"OUTPUT")

while True:
    try:
        # Buzz for 1 second
        grovepi.digitalWrite(buzzer,1)
        print('start')
        time.sleep(1)

        # Stop buzzing for 1 second and repeat
        grovepi.digitalWrite(buzzer,0)
        print('stop')
        time.sleep(1)

    except KeyboardInterrupt:
        grovepi.digitalWrite(buzzer,0)
        break
    except IOError:
        print("Error")