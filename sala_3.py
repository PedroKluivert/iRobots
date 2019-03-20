#!/usr/bin/env python3

from ev3dev.ev3 import *
from time import sleep

gy = GyroSensor('in2')
gy.mode = 'GYRO-ANG'
u = gy.units
us = UltrasonicSensor('in4')
us.mode = 'US-DIST-CM'
motor_esq = LargeMotor('outB')
motor_dir = LargeMotor('outC')
motor_med = MediumMotor('outA')

def Andar_tras():
    motor_dir.run_forever(speed_sp = 500)
    motor_esq.run_forever(speed_sp = 500)

def Andar_frente():
    motor_dir.run_forever(speed_sp = -500)
    motor_esq.run_forever(speed_sp = -500)

def Girar_esq():
    motor_dir.run_forever(speed_sp = -500)
    motor_esq.run_forever(speed_sp = 0)

def Girar_dir():
    motor_dir.run_forever(speed_sp = 0)
    motor_esq.run_forever(speed_sp = -500)

def Parar():
    motor_esq.stop()
    motor_dir.stop()

def Subir_garra():
    motor_med.run_forever(speed_sp=250)

def Descer_garra():
    motor_med.run_forever(speed_sp=-250)

def Parar_garra():
    motor_med.stop()

def Girar_dir_90():
    Giro_Total = 0
    Ang_ant = gy.value()
    while (Giro_Total < 90):
        Girar_dir()
        Giro_Total = gy.value() - Ang_ant
    Parar()

def Girar_esq_90():
    Giro_Total = 0
    Ang_ant = gy.value()
    while (Giro_Total < 90):
        Girar_esq()
        Giro_Total = Ang_ant - gy.value()
    Parar()
'''
Andar_frente()
sleep(4.5)
Parar()
sleep(2)
Andar_tras()
sleep(1)
Parar()
Subir_garra()
sleep(1)
Descer_garra()
sleep(1)
motor_med.stop()
Girar_esq()
sleep(2)
Andar_frente()
sleep(4)
motor_dir.run_forever(speed_sp=0)
motor_esq.run_forever(speed_sp=500)
sleep(3)
Andar_tras()
sleep(1)
Parar()'''


#Percorrer a sala em "Zigue-Zague"
for i in range(2):
    if i==0:
        Girar_dir_90()
    distancia = us.value()/10
    while(distancia > 8):
        Andar_tras()
        distancia = us.value()/10
    Parar()
    sleep(1)
    distancia = us.value()/10
    while(distancia < 82):
        Andar_frente()
        distancia = us.value()/10
    Parar()
    Andar_tras()
    sleep(1)
    Parar()
    sleep(1)
    Subir_garra()
    sleep(1)
    Girar_esq_90()
    Girar_esq_90()
    Andar_tras()
    sleep(1)
    Descer_garra()
    sleep(1)
    while(distancia < 82):
        Andar_frente()
        distancia = us.value()/10
    distancia = us.value()/10
    while(distancia < 82):
        Andar_frente()
        distancia = us.value()/10
    Parar()
    Andar_tras()
    sleep(1)
    Subir_garra()
    Girar_dir_90()
    Girar_dir_90()
    Descer_garra()
    while (distancia < 82):
        Andar_frente()
        distancia = us.value() / 10
    Parar()
