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
L = [gy.value()]

def Corregir(Lista):
    if Lista[0] > gy.value():
        lado = 'direita'
        dife = Lista[0] - gy.value()
        motor_dir.run_to_rel_pos(position_sp=dife, speed_sp=200)
    elif Lista[0] < gy.value():
        lado='esquerda'
        dife = gy.value() - Lista[0]
        motor_esq.run_to_rel_pos(position_sp=dife, speed_sp=200)

ve = 400
i = 0
while True:
    i += 1
    if cor.value()==1:
        print('{} valor: {}'.format(i,gy.value))
        motor_esq.run_forever(speed_sp=ve)
        motor_dir.run_forever(speed_sp=ve)
        dist = us.value()/10
        print("while: ", cor.value())
    if cor.value()!=1:
        Corregir(L)
