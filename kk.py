#!/usr/bin/env python3

#Bibliotecas importadas
from ev3dev.ev3 import *
from time import sleep
import time
import datetime
from simple_pid import PID
import paho.mqtt.client as mqtt

#Sensores do outro brick
sensor_ultra_server = 0
sensor_cor_server = 0

def on_message(client, userdata, message):
    global sensor_cor_server, sensor_ultra_server
    payload = unpack("iid", message.payload)
    sensor_ultra_server = payload[0]
    sensor_cor_server = payload[1]
    #print(payload)


def on_connect(client, userdata, flags, rc):
    print("The robots are connected with result code", str(rc))
    client.subscribe("topic/sensors")


client = mqtt.Client()
client.connect("10.42.0.211", 1883, 60)
client.loop_start()
client.on_connect = on_connect
client.on_message = on_message

#gy = GyroSensor('in2')
# gy.mode = 'GYRO-ANG'
# u = gy.units

# Declaracao de sensores
UltraSonico_1 = UltrasonicSensor('in1') #Sensor que vai ver distancia, auxiliando na locomoção do robo pela sala
UltraSonico_1.mode = 'US-DIST-CM'
UltrasonicoLado = UltrasonicSensor('in3') #Sensor de verificação de área de resgate
UltrasonicoLado.mode = 'US-DIST-CM'
CorDireita = ColorSensor('in2') #Sensor de cor da direita
CorDireita.mode = 'COL-REFLECT'
CorEsquerda = ColorSensor('in4') #Sensor de cor da esquerda.
CorEsquerda.mode = 'COL-REFLECT'
# cl = ColorSensor('in3')
# cl.mode = 'COL-COLOR'

# Declaracao de Motores
Motor_Esquerda = LargeMotor('outB')
Motor_Esquerda.polarity = "inversed"
Motor_Direita = LargeMotor('outC')
Motor_Direita.polarity = "inversed"
MotorMeio_Escavadeira = LargeMotor('outD')


#kp = 178 kd=0.8 ki=0.50 valor default
pid = PID(250, 0, 0, setpoint=4.6)     #sala3
pid2 = PID(10,0, 0, setpoint=0)       #sala1


def Motor_Andar(temp, dir=550, esq=600):
    #Função genérica para andar, passando como parametros o tempo,
    # velocidade da direita e velocidadde da eesquerda

    begin = datetime.datetime.now()
    end = begin + datetime.timedelta(seconds=temp)
    while datetime.datetime.now() <= end:
        Motor_Esquerda.run_forever(speed_sp=esq)
        Motor_Direita.run_forever(speed_sp=dir)
    Parar()

def AndarpelaDistancia(dir=500, esq=450):
    volta = 0
    for i in range(4):
        try:
            Descer_garra()
            distancia = UltraSonico_1.value()/10
            Motor_Andar(6, dir, esq)
            Motor_Andar(1, 300, 300)
            Parar()
            Motor_Andar(1.5, -200, -200)
            Subir_garra()
            if(volta == 0):
                Motor_Andar(4.3, 400, 0)
                volta = 1
            else:
                if i==3:
                    Parar()
                    Descer_garra()
                    Motor_Andar(1.5, -400, 400)
                    Motor_Andar(4, -400, -400)
                else:
                    Motor_Andar(4.1, 0, 400)
                    volta = 0
            Motor_Andar(2, -500, -500)
            Descer_garra()
            sleep(2)
            Subir_garra()
            sleep(2)
            Descer_garra()
        except KeyboardInterrupt:
            Parar()
            Parar_garra()

    Parar()
    Subir_garra()
    DerrubarVitimas()
    Parar()
    Parar_garra()


# Função para andar infinitamente ate que veja a distancia x, utilizando o PID
# Para que ele ande reto, tendo a parede como setpoint
def Motor_Infinito_frente(x):

    #control = pid(us.value())
    #print(control)

    while (UltraSonico_1.value() / 10 > x):

        control = pid(UltrasonicoLado.value()/10)
        if (control > 500):
            control = 500
        elif (control < -500):
            control = -500

        # print(control + 500, 500 - control)

        Motor_Direita.run_forever(speed_sp=500 + control)
        Motor_Esquerda.run_forever(speed_sp=500 - control)

        if UltraSonico_1.value() / 10 < 12: #distancia da parede
             Parar()


#Tentando contornar Obstáculo
def Obstáculo():
    if UltraSonico_1.value() / 10 <= 6:
        return True
    else:
        return False


def Contornar():
    if Obstáculo() == True:
        Motor_Andar(2, 400, -400)
        Motor_Andar(1, 400, 400)
        for i in range(2):
            Motor_Andar(2, -400, 400 )
            Motor_Andar(1, 400, 400)


def Seguir_Linha():
    Subir_garra()
    velocidade = 600

    cont = 0
    CONSTANTE = True
    while CONSTANTE:
        erro = CorDireita.value() - CorEsquerda.value()
        control = pid2(erro)
        if (control > 300):
            control = -300
        elif (control < -300):
            control = 300

        Motor_Direita.run_forever(speed_sp=velocidade + control)
        Motor_Esquerda.run_forever(speed_sp=velocidade - control)


        if (CorEsquerda.value() <= 28) and (CorDireita.value()<=28):
            print(CorDireita, CorEsquerda)
            cont+=1
        if cont == 5:
            print('entrei na sala')
            Parar()
            ProcuraInicial()

        print(control + velocidade, velocidade - control)

        print(UltraSonico_1.value() / 10)

# Função para parar motores esquerdo e direito
def Parar():
    Motor_Esquerda.stop()
    Motor_Direita.stop()

# Função para subir a garra
def Subir_garra():
    MotorMeio_Escavadeira.run_forever(speed_sp=-550)
    sleep(0.9)

# Funcao para descer a garra
def Descer_garra():
    sleep(2)
    MotorMeio_Escavadeira.run_forever(speed_sp=350)

# Função para parar a garra
def Parar_garra():
    MotorMeio_Escavadeira.stop()

# Funcao para girar direita com tempo
def Girar_dir():
    begin = datetime.datetime.now()
    end = begin + datetime.timedelta(seconds=1.25)
    while datetime.datetime.now() <= end:
        Motor_Esquerda.run_forever(speed_sp=0)
        Motor_Direita.run_forever(speed_sp=-500)
    Parar()

# Funcao para girar esquerda com tempo
def Girar_esq():
    begin = datetime.datetime.now()
    end = begin + datetime.timedelta(seconds=1.25)
    while datetime.datetime.now() <= end:
        Motor_Esquerda.run_forever(speed_sp=-500)
        Motor_Direita.run_forever(speed_sp=0)
    Parar()

def Parede():
    Motor_Infinito_frente(12)
    Motor_Andar(3, 300, 300)
    Parar()
    Motor_Andar(0.5, -500, -500)
    Subir_garra()
    Motor_Andar(1.8, 500, 0)
    Descer_garra()

def Pecorrer():
    try:
        Subir_garra()
        sleep(2)
        Motor_Andar(2, -400, 10)
        Motor_Andar(1.5, 250, 300)
        Motor_Andar(1, 400, -10)
        for i in range(4):
            Descer_garra()
            sleep(1)
            Motor_Andar(5)
            Subir_garra()
            sleep(1)
            Motor_Andar(1, -350, -410)
            Motor_Andar(0.5, 200, 260)
            Motor_Andar(1.6, 400, -100)

    except KeyboardInterrupt:
        Parar()
        Parar_garra()



#Funçao para ver a area de resgate
def VerAreaDeResgate():
    Motor_Infinito_frente(7)
    Motor_Andar(1.6, 400, -100)  # girar eixo 90
    sleep(1)

#Funcao para deixqar as vitimas a area de resgate
def DerrubarVitimas():
    Descer_garra()
    for i in range(3):
        Parar()
        Motor_Andar(2, -600, -600)
        Parar()
        Motor_Andar(1.5, 300, 350)
        Parar()
    Parar_garra()


# O robo vai procurar a area de resgate
def ProcuraInicial():
    Subir_garra()
    CONSTANTE = True
    while CONSTANTE:
        try:
            dist2 = UltrasonicoLado.value() / 10
            print(dist2, ' cm')
            VerAreaDeResgate()
            # if (dist2 > 50):
            #     print("Entrei pelo lado esquerdo!")
            #     Motor_Andar(1.5, 200, -200)
            #     Parar()
            #     sleep(2)
            #     Motor_Andar(1, 200, 200)
            #     #ProcuraInicial()
            # dist2 = UltrasonicoLado.value() / 10
            if (dist2 >= 18.5) and (dist2 <= 30):
                Parar()
                Sound.beep()
                print('Vi a area de resgate!')
                AndarpelaDistancia()
                break
            elif(dist2 > 30):
                print('vi bolinha\n', dist2)
                Motor_Andar(2, -400, 400)
                VerAreaDeResgate()
            else:
                pid = PID(250, 0, 0, setpoint=4.6)

        except KeyboardInterrupt:
            Parar()
            Parar_garra()
            CONSTANTE = False


#ProcuraInicial()

#Pecorrer()

Subir_garra()
sleep(2)
Descer_garra()

# Falar
#Sound.speak("HHUULLKK").wait()

print('\nVoces vao conseguir!')
# on_message()
