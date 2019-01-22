#!/usr/bin/env python3

from ev3dev.ev3 import * #biblioteca com os comando do robô
from time import sleep

#Variaveis do sensores:
"""
Tipo de sensores: InfraredSensor(), TouchSensor(), UltrasonicSensor(),GyroSensor(), ColorSensor().
"""

us = UltrasonicSensor('in4')
us.mode = 'US-DIST-CM'
motor_esq = LargeMotor('outC')
motor_dir = LargeMotor('outB')
cor = ColorSensor('in3')
cor.mode = 'COL-COLOR'
gy = GyroSensor('in2')
gy.mode = 'GYRO-ANG'
veloC = 500
l=[]

button = Button()

'''while not button.any():
    motor_dir.run_forever(speed_sp=400)
    motor_esq.run_forever(speed_sp=400)
    sleep(2)
    l.append(gy.value())'''
def parar(tempo):
    motor_dir.stop()
    motor_esq.stop()
    sleep(tempo)


girop = 0
ant1 = gy.value()

while girop<=90:
    dist=us.value()/10
    l.append(dist)
    giro = 0
    ant = gy.value()
    while giro <= 1:
        motor_dir.run_forever(speed_sp=400)
        motor_esq.run_forever(speed_sp=0)
        # if us.value() < 87:
        #     motor_dir.run_forever(speed_sp=400)
        #     motor_esq.run_forever(speed_sp=400)
        #     sleep(3)
        sleep(0.1)
        giro = gy.value() - ant
    girop = ant1 + gy.value()
    print("giro ",girop)
    parar(1)


print(l)
