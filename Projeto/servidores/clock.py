import time
import random

relogio_fisico = 0.0

def get_relogio_fisico():
    global relogio_fisico
    variacao = random.uniform(-1.0, 1.0)
    relogio_fisico += variacao
    if relogio_fisico < 0:
        relogio_fisico = 0
    return round(relogio_fisico, 3)

def set_relogio_fisico(novo_valor):
    global relogio_fisico
    relogio_fisico = novo_valor

relogio_lamport = 0

def get_relogio_lamport():
    return relogio_lamport

def incrementar_lamport():
    global relogio_lamport
    relogio_lamport += 1
    return relogio_lamport

def atualizar_lamport(recebido):
    global relogio_lamport
    relogio_lamport = max(relogio_lamport, recebido) + 1
    return relogio_lamport
