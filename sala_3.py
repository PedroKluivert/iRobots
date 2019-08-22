#!/usr/bin/env python3

from ev3dev.ev3 import *
from time import sleep
import time
import datetime
from simple_pid import PID

# gy = GyroSensor('in2')
# gy.mode = 'GYRO-ANG'
# u = gy.units
us = UltrasonicSensor('in1')
us.mode = 'US-DIST-CM'
motor_esq = LargeMotor('outB')
motor_dir = LargeMotor('outA')
motor_med = MediumMotor('outD')
us2 = UltrasonicSensor('in3')
us2.mode = 'US-DIST-CM'

#kp = 178 kd=0.8 ki=0.50 valor default
pid = PID(250, 0, 0, setpoint=4.8)

# cl = ColorSensor('in3')
# cl.mode = 'COL-COLOR'
# Função andar para frente por 2.5seg

def Motor_Andar(temp, dir, esq=600):
    begin = datetime.datetime.now()
    end = begin + datetime.timedelta(seconds=temp)
    while datetime.datetime.now() <= end:
        motor_esq.run_forever(speed_sp=esq)
        motor_dir.run_forever(speed_sp=dir)
    Parar()

#Nao ta funcionando essa funcao de giro
def girar(sentido, giro=360, velocidade=300):
    if(sentido == 'esquerda'):
        motor_esq.run_to_rel_pos(position_sp=giro, speed_sp=300)
        motor_dir.run_to_rel_pos(position_sp=-giro, speed_sp=-300)
    if(sentido == 'direita'):
        motor_esq.run_to_rel_pos(position_sp=-giro, speed_sp=-300)
        motor_dir.run_to_rel_pos(position_sp=giro, speed_sp=300)

def GirarGiroscopio(sentido, grau):
    Total = 0
    if(sentido == 'esquerda'):
        Ang_ant = gy.value()
        while(Total < grau):
            motor_esq.run_forever(speed_sp=300)
            motor_dir.run_forever(speed_sp=-300)
            Total = gy.value() - Ang_ant
        Parar()
    if(sentido == 'direita'):
        Ang_ant = gy.value()
        while (Total < grau):
            motor_esq.run_forever(speed_sp=-300)
            motor_dir.run_forever(speed_sp=300)
            Total = Ang_ant - gy.value()
        Parar()


# Função para andar infinito
def Motor_Infinito_frente(x):

    #control = pid(us.value())
    #print(control)

    while (us.value() / 10 > x):

        control = pid(us2.value()/10)
        if (control > 500):
            control = 500
        elif (control < -500):
            control = -500

        # print(control + 500, 500 - control)

        motor_dir.run_forever(speed_sp=500 + control)
        motor_esq.run_forever(speed_sp=500 - control)

        if us.value() / 10 < 12: #distancia da parede
             Parar()



def Motor_Infinito_tras():
    while us.value() / 10 > 15:
        motor_dir.run_forever(speed_sp=-500)
        motor_esq.run_forever(speed_sp=-500)
        if us.value() / 10 < 10:
            Parar()


# Função para parar
def Parar():
    motor_esq.stop()
    motor_dir.stop()

# Função para subir a garra
def Subir_garra():
    motor_med.run_forever(speed_sp=-450)
    sleep(2)

# Função para descer a garra
def Descer_garra():
    motor_med.run_forever(speed_sp=450)
    sleep(2)

# Função para parar a garra
def Parar_garra():
    motor_med.stop()

def Girar_dir():
    begin = datetime.datetime.now()
    end = begin + datetime.timedelta(seconds=1.25)
    while datetime.datetime.now() <= end:
        motor_esq.run_forever(speed_sp=0)
        motor_dir.run_forever(speed_sp=-500)
    Parar()

def Girar_esq():
    begin = datetime.datetime.now()
    end = begin + datetime.timedelta(seconds=1.25)
    while datetime.datetime.now() <= end:
        motor_esq.run_forever(speed_sp=-500)
        motor_dir.run_forever(speed_sp=0)
    Parar()

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

def Andar_frente(x):
    dist = us.value()/10
    while dist>=x:
        print(dist)
        motor_esq.run_forever(speed_sp=500)
        motor_dir.run_forever(speed_sp=500)
        if dist<x:
            motor_esq.stop()
            motor_dir.stop()

def Percorrer():
    volta = 0
    for i in range(4):
        Descer_garra()
        Parar()
        Motor_Andar(4.8, 650, 650) #andar frente
        sleep(1)
        Motor_Andar(1, -200, -200)
        Subir_garra()
        if(volta == 0):
            if i ==3:
                Parar()
                Motor_Andar(2, -400, 400)
                Motor_Andar(5, -400, -400)
            else:
                Motor_Andar(6, 400, 0)
                volta = 1
        elif(volta == 1):
            if i ==3:
                Parar()
                Motor_Andar(2, -400, 400)
                Motor_Andar(5, -400, -400)
            else:
                Motor_Andar(6, 0, 400)
                volta = 0
        Motor_Andar(2, -400, -400)

    Parar()
    Parar_garra()

def VerAreaDeResgate():
    Subir_garra()
    dist = us.value() / 10
    Motor_Infinito_frente(12)
    Motor_Andar(2.2, 400, -100)  # girar eixo 90
    sleep(1)

CONSTANTE = True
while CONSTANTE:
    try:
         dist2 = us2.value() / 10
         print(dist2, ' cm')
         VerAreaDeResgate()
         if (dist2 >= 18.5):
             Parar()
             Sound.beep()
             print('Vi a area de resgate!')
             Percorrer()
             break
         else:
             pid = PID(250, 0, 0, setpoint=4.6)

    except KeyboardInterrupt:
        Parar()
        Parar_garra()
        CONSTANTE = False

print('\nVoces vao conseguir!')

# for i in range(3):
#     motor_esq.run_forever(speed_sp=-1000)
#     motor_dir.run_forever(speed_sp=-1000)
#     Parar()
#     motor_esq.run_forever(speed_sp=300)
#     motor_dir.run_forever(speed_sp=300)
#     sleep(1)
#     Parar()
# Parar_garra()

