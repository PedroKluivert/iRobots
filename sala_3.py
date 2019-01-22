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

while True:
    motor_dir.run_forever(speed_sp=400)
    motor_esq.run_forever(speed_sp=400)
    sleep(3)
    ant = gy.value()
    giro = 0
    while giro <=80:
        giro=gy.value() - ant
        print(giro,gy.value(),ant)
        motor_dir.run_forever(speed_sp=400)
        motor_esq.run_forever(speed_sp=0)
    motor_dir.stop()



