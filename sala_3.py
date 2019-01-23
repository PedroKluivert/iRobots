#!/usr/bin/env python3

from ev3dev.ev3 import * #biblioteca com os comando do robô
from time import sleep


us = UltrasonicSensor('in4')
us.mode = 'US-DIST-CM'
motor_esq = LargeMotor('outB')
motor_dir = LargeMotor('outC')
cor = ColorSensor('in3')
cor.mode = 'COL-COLOR'
gy = GyroSensor('in2')
gy.mode = 'GYRO-ANG'
button = Button()
VELOC = 400

def andar_frente(v):    #função para andar pra frente; 'v': velocidade
    motor_dir.run_forever(speed_sp=v)
    motor_esq.run_forever(speed_sp=v)


def giro_esq(v):    #função girar o brickman para esquerda
    motor_dir.run_forever(speed_sp=v)
    motor_esq.run_forever(speed_sp=0)


def giro_dir(v):    #função girar o brickman para direita
    motor_dir.run_forever(speed_sp=0)
    motor_esq.run_forever(speed_sp=v)

def parar(tempo):       #função para parar
    motor_dir.stop()
    motor_esq.stop()
    sleep(tempo)


def andar_tras(v):    #função para andar pra tras; 'v': velocidade
    motor_dir.run_forever(speed_sp=-v)
    motor_esq.run_forever(speed_sp=-v)

l_d = []
l_a = []
giroT = 0
ang_ant = gy.value()

while (giroT < 70):       #loop para mover em 90 Graus
    dist = us.value()/10
    l_d.append(dist)
    giro_i = 0
    ang_i = gy.value()
    while giro_i < 1:    #loop para mover em pequenos graus
        giro_dir(VELOC)
        sleep(0.1)
        giro_i = gy.value() - ang_i   # mudando o referencial do loop interno
    giroT = gy.value() - ang_ant      # mudando o referencial do loop externo
    l_a.append(gy.value())
    parar(1)

md = min(l_d)                    # menor distancia
i_md = l_d.index(md)             # indice da menor distancia
a_md = l_a[i_md]                 # angulo da menor distancia
ult_a = l_a[len(l_a)-1]          # ultimo angulo da lista
volte = ult_a - a_md             # voltar a menor distancia

print('Distancias:\n {}'.format(l_d))
print('Angulos:\n {}'.format(l_a))
print('Volte {} graus.'.format(volte))


ang_ant = gy.value()
giroT = 0
while (giroT < volte):
    giro_esq(VELOC)
    giroT = ang_ant - gy.value()
parar(1)


