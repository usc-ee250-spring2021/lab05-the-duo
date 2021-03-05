"""EE 250L Lab 04 Starter Code
Jeffrey Liu
Aaron Sesay
https://github.com/usc-ee250-spring2021/lab05-the-duo.git
Run vm_subscriber.py in a separate terminal on your VM."""

import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    #subscribe to the ultrasonic ranger topic here
    client.subscribe("sesay/ultrasonicRanger")
    client.message_callback_add("sesay/ultrasonicRanger", mycallback)
    client.subscribe("sesay/button")
    client.message_callback_add("sesay/button", buttoncallback)


#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))
def mycallback(client,userdata,msg):
    print("VM:" + str(msg.payload, "utf-8") + "cm")
def buttoncallback(client,userdata,msg):
    decode = str(msg.payload, "utf-8")
    print(decode)
    if decode == "1":
        print("Button Pressed!")
    #if decode != "1":
     #   print("Nothing")

if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()

    while True:
        #print("delete this line")
        time.sleep(1)