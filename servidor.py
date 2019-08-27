#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import ev3dev.ev3 as ev3
from struct import *
from datetime import datetime, timedelta
import time



def on_publish(client,userdata,result):             #create function for callback
    print("data published \n")
    pass

client = mqtt.Client()
client.on_publish = on_publish

client.connect("localhost", 1883, 60)

#ultrasonic = ev3.UltrasonicSensor("in1")
#color_sensor = ev3.ColorSensor("in2")


client.loop_start()


try:
    while True:
        message = pack("iid", 0, 0, time.time())
        client.publish("topic/sensors", message, qos=0)
        print(unpack("iid", message))
        time.sleep(0.1)

except KeyboardInterrupt:
    pass


client.loop_end()
client.disconnect()