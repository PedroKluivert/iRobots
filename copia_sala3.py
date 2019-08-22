# !/usr/bin/env python3
from ev3dev.ev3 import *

print("configuracao de portas e modos")
from portas_modos import *

print("json")
from json import load

from time import sleep
import time
import datetime

gy = GyroSensor('in2')
gy.mode = 'GYRO-ANG'
u = gy.units
us = UltrasonicSensor('in4')
us.mode = 'US-DIST-CM'
motor_esq = LargeMotor('outB')
motor_dir = LargeMotor('outC')
garra = MediumMotor('outA')
cl = ColorSensor('in3')
cl.mode = 'COL-COLOR'


# lado do sensor de lado, isso vai definir por onde o robo vai ultrapassar o
# obstaculo e as motor_direcoes que ele vai tomar quando dentro da sala 3, na busca
# de vitimas, por exemplo
lado_us = 'motor_esquerda'

# pra se orientar na sala 3 em funcao do lado que o sensor estah, deve-se
# definir o lado que o sensor nao estah tambem
if lado_us == 'motor_esquerda':
    lado_contrario_us = 'motor_direita'
elif lado_us == 'motor_direita':
    lado_contrario_us = 'motor_esquerda'


def guardar_garra():
    """Guarde a garra em cima do brick pra quando nao estiver utilizando ela.
    TODA VEZ QUE GUARDAR A GARRA, DEFINA O VALOR DE estado_garra PRA 'guardada'.
    """

    garra.run_timed(time_sp=3000, speed_sp=-120, stop_action='coast')

    # espere acabar de guardar
    garra.wait_while('running')

    # esperar a garra chegar ao repouso em cima do brick
    sleep(1)

    print('a garra estah guardada')


def abaixar_garra():
    """Abaixe a garra pra pegar bola.
    TODA VEZ QUE ABAIXAR A GARRA, DEFINA O VALOR DE estado_garra PRA 'abaixada'.
    """

    garra.run_timed(stop_action='hold', time_sp=5000, speed_sp=400)

    # espere acabar de abaixar
    garra.wait_while('running')
    print('a garra estah abaixada')


# colocar a garra num estado conhecido
guardar_garra()
estado_garra = 'guardada'

# o robo inicia este programa com a garra guardada, isto eh, em cima do brick e
# sem forca pra ativamente mante-la em cima do brick; o abaixo definido eh uma
# especie de calibracao.
# zero eh a posicao da garra guardada.
garra.position = 0


# abaixar_garra()
# estado_garra = 'abaixada'



def graus_robo_para_tacho_counts_motores(graus):
    """Retorne quanto de tacho counts os motores giram o robo dados `graus`.

    Para girar(), eh util que quem chame diga quantos graus quer que o robo
    gire. No entanto, como nao temos um giroscopio, fazemos isso mandando um
    valor em tacho counts pra os dois motores, um girando em reverso, outro
    girando normalmente, isso faz com que o robo gire em seu proprio eixo.

    Esta funcao faz o trabalho de retornar o valor em tacho counts que eh
    preciso mandar pra os motores pra girar o robo dados `graus`.
    Note que, como nao temos um giroscopio, usamos um valor que sabemos que o
    robo gira 90 graus, por olhometro, e usamos ele como referencia pra regra
    de tres que realiza a conversao. Este valor eh definido abaixo, pra
    facilitar caso precise de ajuste.
    """

    # valor de referencia de 90 graus, tc eh abreviacao de tacho counts

    # o valor de giro para girar 90 graus eh diferente se a garra estah
    # abaixada ou guardada, pois o centro de gravidade eh movido
    if estado_garra == 'guardada':
        giro_noventa_graus_em_tc = 400
    elif estado_garra == 'abaixada':
        giro_noventa_graus_em_tc = 282.5

    # tc eh abreviacao de tacho counts
    valor_tc = (giro_noventa_graus_em_tc * graus) / 90

    return valor_tc


def girar(sentido, graus=90, velocidade=300):
    """Gire o robo no proprio eixo tantos `graus` no dado `sentido`.

    Parametros:
    `sentido` (string, 'motor_esquerda' ou 'motor_direita', case sensitive)
        eh o sentido que o robo gira;
    `graus` (float, por padrao 90)
        eh o tanto de graus que robo gira;
    `velocidade` (float, por padrao 300)
        eh a velocidade que o robo gira.
    """

    # para uma explicacao disso, vide a definicao da funcao abaixo
    giro = graus_robo_para_tacho_counts_motores(graus)

    if sentido == 'motor_esquerda' and giro < 0:
        giro *= -1
    elif sentido == 'motor_direita' and giro > 0:
        giro *= -1

    # com giro positivo, isso abaixo gira pra motor_esquerda
    motor_motor_dir.run_to_rel_pos(position_sp=-giro, speed_sp=velocidade)
    motor_motor_esq.run_to_rel_pos(position_sp=giro, speed_sp=velocidade)

    # espera ate acabar
    motor_esq.wait_while('running')


# pra teste
# girar('motor_esquerda', 360)

def andar(distancia_rot, velocidade=100, sentido='frente', esperar_acabar=True):
    """Faca o robo andar com os parametros informados.
    distancia_rot (float): distancia, dada em rotacoes;
    velocidade (inteiro): em rotacoes/segundo;
    sentido (string): 'frente' ou 'tras', case insensitive;
    """

    # O robo, montado como estah, vai pra frente com distancia negativa e pra
    # tras com distancia positiva. O condicional abaixo faz com que ele sempre
    # ande no sentido desejado.
    if sentido.lower() == 'frente' and distancia_rot > 0:
        distancia_rot *= -1
    elif sentido.lower == 'tras' and distancia_rot < 0:
        distancia_rot *= -1

    # convertendo de rotacoes para o que o robo aceita, tacho counts
    tacho_counts = motor_dir.count_per_rot * distancia_rot

    # bote pra andar
    motor_dir.run_to_rel_pos(position_sp=tacho_counts, speed_sp=velocidade)
    motor_esq.run_to_rel_pos(position_sp=tacho_counts, speed_sp=velocidade)

    # espere acabar de andar
    if esperar_acabar == True:
        motor_esq.wait_while('running')


# pra testar
# andar(0.5, esperar_acabar=False)

def tem_obstaculo_no_lado():
    """Retorne (booleano) se o sensor do lado (us) ve obstaculo."""

    if us.distance_centimeters < 30:
        return True
    else:
        return False


def andar_ate_deixar_de_ver_obstaculo():
    """Nome autoexplicativo."""

    # ande eternamente
    motor_dir.run_forever(speed_sp=-80)
    motor_esq.run_forever(speed_sp=-80)

    # pare a execucao do codigo ate que obstaculo nao seja visto
    while tem_obstaculo_no_lado():
        pass

    # pare de andar
    motor_dir.stop()
    motor_esq.stop()


def andar_ate_ver_obstaculo():
    """Nome autoexplicativo."""

    # ande eternamente
    motor_dir.run_forever(speed_sp=-80)
    motor_esq.run_forever(speed_sp=-80)

    # pare a execucao do codigo ate que obstaculo seja visto
    while not tem_obstaculo_no_lado():
        pass

    # pare de andar
    motor_dir.stop()
    motor_esq.stop()




def parar():
    """Para os motores da esteira imediatamente."""

    motor_dir.stop()
    motor_esq.stop()


def andar_pra_sempre(sentido='frente', velocidade=200):
    """Ande pra sempre pra frente.
    Para parar, use parar().
    """

    # O robo, montado como estah, vai pra frente com velocidade negativa e pra
    # tras com velocidade positiva. O condicional abaixo faz com que ele sempre
    # ande no sentido desejado.
    if sentido.lower() == 'frente' and velocidade > 0:
        velocidade *= -1
    elif sentido.lower == 'tras' and velocidade < 0:
        velocidade *= -1

    motor_dir.run_forever(speed_sp=velocidade)
    motor_esq.run_forever(speed_sp=velocidade)


# pra teste
# andar_pra_sempre(sentido='tras')

def tem_linha_se_aproximando(amostras):
    """Retorne se ha pontos se aproximando continuamente.
    Pois isso eh um receptor de bolas no final do outro lado da sala 3.
    """


def tem_linha_se_afastando(amostras):
    """Retorne se ha pontos se afastando continuamente.
    Pois isso eh um receptor de bolas no comeco do outro lado da sala 3.
    """


def tem_receptor_na_minha_frente():
    """Retorne booleano se ha o receptor de vitimas na minha frente.
    Essa funcao deve ser executada quando um provavel receptor estiver na
    frente do robo, isto eh, quando o robo estiver de frente para algum dos
    cantos.
    A logica eh: Se tiver o receptor na minha frente, quando eu andar pro meio
    da pista, vou ver um vazio no lado. No entanto, se eu nao tiver vendo o
    receptor, quando olhar pro lado a partir do meio, vou ver a parede da sala
    imediatamente do meu lado.
    """

    girar(lado_contrario_us)

    # andar ate mais ou menos o meio
    andar(2)
    parar()
    sleep(0.2)

    # olhar pro lado
    lado = us.distance_centimeters

    # se tiver mais que 20 cm no lado, eu tava na frente dum receptor
    if lado > 20:
        tava_na_minha_frente = True
    else:
        tava_na_minha_frente = False

    return tava_na_minha_frente


def andar_ate_bola():
    """Anda em motor_direcao a uma possivel bola, parando quando acha que ve."""

    print('to indo pra bola')

    andar_pra_sempre()

    while sensor_frente.distance_centimeters > 10:
        pass

    parar()
    sleep(2)


def levantar_garra():
    """Levante a garra e pare-a no ar, deixando-a na horizontal para as bolas cairem.

    LEMBRE-SE DE QUE levantar_garra() EH UM ESTADO TEMPORARIO, isto eh, o robo
    nao vai ficar pra sempre com a garra levantada. Logo que ele levanta, deve
    esperar um pouco e guardar_garra().
    """

    # 28 eh a posicao de despejo quando 0 eh a posicao de `guardada`
    garra.run_to_abs_pos(position_sp=28, speed_sp=100, stop_action='hold')

    # espera acabar de levantar a garra
    garra.wait_while('running')

    print('garra estah LEVANTADA')


# pra testar
# levantar_garra()

def pegar_bola():
    """Articule a garra pra capturar uma bola na frente."""

    print('vou pegar bola')

    andar(0.5, sentido='frente')

    # dar meia volta
    #girar('motor_esquerda')
    #girar('motor_esquerda')

    andar(0.6, sentido='frente')

    # ABAIXAR GARRA
    # potencia por dois segundos
    garra.run_timed(time_sp=8000, speed_sp=400, stop_action='hold')
    estado_garra = 'abaixada'

    # espere acabar de baixar a garra
    garra.wait_while('running')

    # da uma rezinha pra garantir que uma bola meia boca entra
    andar(0.5, sentido='tras')
    # compensar a rezinha
    andar(0.5)

    # fazer o mesmo da rezinha, mas pra frente
    andar(0.5)
    andar(0.5, sentido='tras')

    # dar umas giradas pra garantir mesmo
    girar('motor_esquerda', 10)
    girar('motor_direita', 20)
    girar('motor_esquerda', 10)


# pra testar
# pegar_bola()

def investigar_bola():
    """Realize uma busca cautelosa e deixe o robo preparado pra ir buscar a bola."""

    andar(0.5, sentido='tras')

    andar(1, velocidade=100, esperar_acabar=False)

    amostras_detalhadas = []
    while motor_esq.is_running:
        distancia_posicao = (us.distance_centimeters, motor_esq.position)
        amostras_detalhadas.append(distancia_posicao)

    print('VALORES INVESTIGADOS:', distancia_posicao)
    menor_distancia = 1000
    menor_amostra = None
    for amostra in amostras_detalhadas:
        # se distancia da `amostra` (indice 0), for menor que a menor, ela eh a menor
        if amostra[0] < menor_distancia:
            menor_distancia = amostra[0]
            menor_amostra = amostra

    # peguei a menor distancia, peguei a posicao que ela foi vista, sei pra onde ir
    menor_posicao = menor_amostra[1]
    andar_pra_sempre(sentido='tras', velocidade=100)
    margem_erro = 1
    while not motor_esq.position in range(menor_posicao - margem_erro, menor_posicao + margem_erro):
        pass
    parar()

    print('opa, alinhei o us com a vitima')
    sleep(0.5)


def procurar_bola():
    """Realize o caminho de procura de bolas.
    Esta funcao deve ser chamada logo depois do robo perceber que viu o
    receptor de vitimas.
    """

    print('\n -- PROCURANDO BOLA -- \n')

    # voltar pra frente do receptor
    andar(2, sentido='tras')

    # se colocar em posicao de procura
    girar(lado_contrario_us)

    # pra ter uma orientacao
    amostra_atual = us.distance_centimeters

    # comecar a procurar
    andar(4, esperar_acabar=False)

    while motor_esq.is_running or not sensor_frente.distance_centimeters < 5:

        print('escaneando')
        print('AMOSTRAS SENSOR LADO ATUAL:', amostra_atual)
        amostra_anterior = amostra_atual
        amostra_atual = us.distance_centimeters

        if (amostra_anterior - amostra_atual) > 15:
            # opa, discrepancia grande
            print('amostra atual:', amostra_atual)
            print('amostra_anterior', amostra_anterior)
            print('\n -- VI BOLA! -- \n')
            Sound.beep()

            parar()
            sleep(0.5)

            # alinhar o us com a bola
            investigar_bola()

            # alinhar o eixo de giro do robo com a bola
            andar(0.2, sentido='tras')

            # se colocar na motor_direcao da captura
            girar(lado_us)

            andar_ate_bola()
            pegar_bola()
            break

    print('acabei de escanear')


def andar_ate_proximo_canto():
    """Anda ate o sensor_frente ver menos que 10."""

    andar_pra_sempre()

    while sensor_frente.distance_centimeters > 10:
        pass


def depositar_bola():
    """Com alguma bola na cacamba, volte pro receptor pra deixar a bola nele."""

    andar_ate_proximo_canto()
    girar(lado_contrario_us, -20)

    # gira pra parede
    girar(lado_us, 20)

    # anda ate receptor
    andar_ate_proximo_canto()

    # gira pra ficar do lado do receptor
    girar(lado_contrario_us, 40)

    # anda pra ficar no centro do lado do receptor
    andar(0.5)
    levantar_garra()


def rotina_sala_3():
    """Faca a sala 3.
    A partir do inicio da sala 3, logo apos a deteccao da silver tape, essa
    funcao assume.
    """

    # coloque-se inteiro na sala 3
    andar(1.4)

    # sobre que lado entramos na sala 3
    if us.distance_centimeters > 30:
        # se o us ve muito, ele olha pro meio, entramos pelo lado
        # oposto a ele na sala 3

        # gira pra andar rente a parede
        girar(lado_us)

        # anda pra nao ver a entrada da sala 3 com o sensor de lado e girar
        # de novo
        andar(2)

    # girar bem pouquinho pro lado do sensor pra que o robo ante arrastando na
    # parede
    girar(lado_us, 20)

    for canto in range(3):
        print('vou pro proximo canto pela', canto + 1, 'vez')
        andar_ate_proximo_canto()

        if tem_receptor_na_minha_frente():
            Sound.beep().wait()
            Sound.beep().wait()
            print('opa, receptor tava na minha frente')
            #procurar_bola()
            #depositar_bola()
            break

        else:
            print('opa, receptor NAO tava na minha frente')

    print('nao vi nenhum receptor :/')
    parar()
    sleep(20)


# pra teste
# rotina_sala_3()




def get_valor_sensor_motor_direita():
    """Retorne o valor do sensor motor_direito convertido para a escala de 0-1000."""

    valor = (
                    (motor_direita["branco"] - sensor_motor_dir.value()) /
                    (motor_direita["branco"] - motor_direita["preto"])
            ) * -1000 + 1000

    return valor


def get_valor_sensor_motor_esquerda():
    """Retorne o valor do sensor motor_esquerdo convertido para a escala de 0-1000."""

    valor = (
                    (motor_esquerda["branco"] - sensor_motor_esq.value()) /
                    (motor_esquerda["branco"] - motor_esquerda["preto"])
            ) * -1000 + 1000

    return valor


def seguir_parede():
    """Ande rente a parede da motor_direita ate que encontre algo na frente, usando o sensor de lado."""

    andar_pra_sempre()

    while sensor_frente.distance_centimeters > 10:
        andar_pra_sempre()
        sleep(0.4)

        lado = us.distance_centimeters
        distancia = 6
        if lado < distancia:
            girar('motor_esquerda', 10)
        else:
            girar('motor_direita', 10)

    parar()


# pra testar
# seguir_parede()

def relaxar_garra():
    """Solte forca da garra."""

    garra.stop(stop_action='coast')


def vejo_silver_tape():
    """Retorne booleano se os sensores de reflectancia veem a silver tape.
    O intervalo que define se a reflectancia atual eh a de silver tape eh
    calibrado previamente e entao eh consultado aqui.
    """

    if sensor_motor_dir.value() in range(motor_direita['silver_tape_min'], motor_direita['silver_tape_max']) \
            and sensor_motor_esq.value() in range(motor_esquerda['silver_tape_min'], motor_esquerda['silver_tape_max']):

        # anda um pouco e verifica de novo
        andar(0.1)
        return sensor_motor_dir.value() in range(motor_direita['silver_tape_min'], motor_direita['silver_tape_max']) \
               and sensor_motor_esq.value() in range(motor_esquerda['silver_tape_min'], motor_esquerda['silver_tape_max'])

    else:
        return False