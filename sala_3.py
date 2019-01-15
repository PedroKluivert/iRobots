#!/usr/bin/env python3

#Author: Wanderson Hermirio and Josenildo Simão
#Site de Consulta: https://sites.google.com/site/ev3python/learn_ev3_python/

#biblioteca principais para o funcionamentos do robô
from ev3dev.ev3 import * #biblioteca com os comando do robô
from time import sleep

#variaveis do sensores
"""
tipo de sensores: InfraredSensor(), TouchSensor(), UltrasonicSensor(),GyroSensor(), ColorSensor().
"""

#sensor_fre = UltrasonicSensor('in1') #Especifica qual o sensor esta usando
#sensor_esq = ColorSensor('in2') #Especifica qual o sensor esta usando
#sensor_dir = ColorSensor('in3') #Especifica qual o sensor esta usando


#modo do senso
#sensor_fre.mode = 'US-DIST-CM'

#variaveis do motor
"""
tipo de Motor:  MediumMotor()
                LargeMotor()
"""
us = UltrasonicSensor('in4')
us.mode = 'US-DIST-CM'
motor_esq = LargeMotor('outC')
motor_dir = LargeMotor('outB')

ve_me = 600
ve_md = 600
#modo dos sensores e motores
tempo = 0
#Run
while True:

    # ande eternamente
    motor_esq.run_forever(speed_sp=ve_me)
    motor_dir.run_forever(speed_sp=ve_md)
    dist = us.value()/10
    print(dist)
    if dist <= 15:
        motor_esq.run_forever(speed_sp=-ve_me)
        motor_dir.run_forever(speed_sp=-ve_md)
        sleep(0.5)
        motor_esq.run_forever(speed_sp=0)
        motor_dir.run_forever(speed_sp=ve_md)
        sleep(0.7)
    tempo += 1

