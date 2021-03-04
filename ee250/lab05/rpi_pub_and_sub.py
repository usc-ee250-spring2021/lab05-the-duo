"""EE 250L Lab 04 Starter Code

Run rpi_pub_and_sub.py on your Raspberry Pi."""

import paho.mqtt.client as mqtt
import time
import grovepi


ultrasonicRanger = 0

button = 4


grovepi.pinMode(button,"INPUT")

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    #subscribe to topics of interest here
    client.subscribe("sesay/led")
    client.message_callback_add("sesay/led", ledcallback)
def ledcallback(client,userdata,msg):
    x = str(msg.payload, "utf-8")
    if x == "LED_ON":
        grovepi.digitalWrite(led,1)
    if x == "LED_OFF": 
        grovepi.digitalWrite(led,0)


    client.subscribe("sesay/defaultCallback")


#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()

    while True:
         
        #print("delete this line")
        y = grovepi.ultrasonicRead(ultrasonicRanger)
        z = str(y)
        buttonpress = grovepi.digitalRead(button)
        buttonstring = str(buttonpress)
        client.publish("sesay/button",buttonstring)
     
        client.publish("sesay/ultrasonicRanger", z)
        time.sleep(1)
            

