#!/usr/bin/env python3

from ev3dev.ev3 import *
#from time import sleep
import time
import datetime

gy = GyroSensor('in2')
gy.mode = 'GYRO-ANG'
u = gy.units
us = UltrasonicSensor('in4')
us.mode = 'US-DIST-CM'
motor_esq = LargeMotor('outB')
motor_dir = LargeMotor('outC')
motor_med = MediumMotor('outA')
cl = ColorSensor('in3')
cl.mode = 'COL-COLOR'

#Função andar para frente por 2.5seg

def Andar_frente():
    begin = datetime.datetime.now()
    end = begin + datetime.timedelta(seconds=3.0)
    while datetime.datetime.now() <= end:
        motor_esq.run_forever(speed_sp=600)
        motor_dir.run_forever(speed_sp=600)
    Parar()

#Função andar para frente por 1seg
def Andar_2():
    begin = datetime.datetime.now()
    end = begin + datetime.timedelta(seconds=1.7)
    while datetime.datetime.now() <= end:
        motor_esq.run_forever(speed_sp=600)
        motor_dir.run_forever(speed_sp=600)
    Parar()

#Função andar para trás por 1seg
def Andar_3():
    begin = datetime.datetime.now()
    end = begin + datetime.timedelta(seconds=1)
    while datetime.datetime.now() <= end:
        motor_esq.run_forever(speed_sp=-600)
        motor_dir.run_forever(speed_sp=-600)
    Parar()

#Função andar para trás por 2.5seg
def Andar_tras():
    begin = datetime.datetime.now()
    end = begin + datetime.timedelta(seconds=2.5)
    while datetime.datetime.now() <= end:
        motor_esq.run_forever(speed_sp=-600)
        motor_dir.run_forever(speed_sp=-600)
    Parar()

#Girar para direita
def Girar_dir():
    begin = datetime.datetime.now()
    end = begin + datetime.timedelta(seconds=1.25)
    while datetime.datetime.now() <= end:
        motor_esq.run_forever(speed_sp=0)
        motor_dir.run_forever(speed_sp=-500)
    Parar()

def Girar_dir_eixo_180():
    begin = datetime.datetime.now()
    end = begin + datetime.timedelta(seconds=2.5)
    while datetime.datetime.now() <= end:
        motor_esq.run_forever(speed_sp=0)
        motor_dir.run_forever(speed_sp=-600)
    Parar()

#Função girar para esquerda

def Girar_esq():
    begin = datetime.datetime.now()
    end = begin + datetime.timedelta(seconds=1.25)
    while datetime.datetime.now() <= end:
        motor_esq.run_forever(speed_sp=-500)
        motor_dir.run_forever(speed_sp=0)
    Parar()

#Função para parar
def Parar():
    motor_esq.stop()
    motor_dir.stop()

#Função para subir a garra
def Subir_garra():
    motor_med.run_forever(speed_sp=250)

#Função para descer a garra
def Descer_garra():
    motor_med.run_forever(speed_sp=-250)

#Função para parar a garra
def Parar_garra():
    motor_med.stop()

#Função para girar para direita em 90 graus
def Girar_dir_90():
    Giro_Total = 0
    Ang_ant = gy.value()
    while (Giro_Total < 90):
        Girar_dir()
        Giro_Total = gy.value() - Ang_ant
    Parar()

#Função para girar para esquerda em 90 graus
def Girar_esq_90():
    Giro_Total = 0
    Ang_ant = gy.value()
    while (Giro_Total < 90):
        Girar_esq()
        Giro_Total = Ang_ant - gy.value()
    Parar()

#Função para girar para esquerda em 45 graus
def Girar_esq_45():
    Giro_Total = 0
    Ang_ant = gy.value()
    while (Giro_Total < 45):
        Girar_esq()
        Giro_Total = gy.value() - Ang_ant
    Parar()

#Função iniciar para saber por qual entrada o robô vai entrar
def entrada():
    print(us.value())
    if us.value()>=20:
        direita()
    else:
        esquerda()

#Função para indentificar a área de resgate se entrar pela direita
def direita():
    cont=0
    for i in range(3):
        Andar_frente()
        Parar()
        Girar_esq()
        print(cl.value())
        if(cl.value()==1):
            cont+=1
        else:
            print('Nao esta nessa ponta.')
        Andar_2()
        Girar_esq()
    Andar_frente()
    if(cont==1):
        print('Zigue-zague1')
        #contador1()
    elif(cont==2):
        print('Zigue-zague2')
        #contador2()
    elif(cont==3):
        print('Zigue-zague3')
        #contador3()
    else:
        print('A area de resgate nao foi detectada')


#Função para indentificar a área de resgate se entrar pela esquerda
def esquerda():
    Girar_esq_90()
    cont = 0
    for i in range(3):
        Andar_tras()
        Girar_dir()
        print(cl.value())
        if cl.value() == 1:
            cont += 1
        Andar_3()
    Andar_tras()
    if cont==1:
        print('zigue-zague4')
        #contador4()
    elif cont==2:
        print('zigue-zague5')
        #contador5()
    elif cont==3:
        print('zigue-zague6')
        #contador6()


entrada()


















'''Andar_frente()
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
Parar()
'''
'''# Percorrer a sala em "Zigue-Zague"
for i in range(2):
    if i == 0:
        Girar_dir_90()
    distancia = us.value() / 10
    while (distancia > 8):
        Andar_tras()
        distancia = us.value() / 10
    Parar()
    sleep(1)
    distancia = us.value() / 10
    while (distancia < 82):
        Andar_frente()
        distancia = us.value() / 10
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
    while (distancia < 82):
        Andar_frente()
        distancia = us.value() / 10
    distancia = us.value() / 10
    while (distancia < 82):
        Andar_frente()
        distancia = us.value() / 10
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
    Parar()'''
'''L1=[75,80,75]
Subir_garra()
L2 = []
preto =0
for i in range(3):
    if i ==0:
        Girar_esq_90()
        sleep(2)
        L2.append(us.value()/10)
    else:
        Girar_esq_45()
        sleep(2)
        L2.append(us.value()/10)
    if (L2[i] < L1[i]):
        preto = i+1

print(L1)
print(L2)
print(preto)'''

