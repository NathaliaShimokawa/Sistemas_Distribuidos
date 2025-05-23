import time
import random

# ========== RELÓGIO FÍSICO ==========
relogio_fisico = 0.0

def get_relogio_fisico():
    """
    Simula um relógio físico com variação aleatória entre -1s e +1s.
    """
    global relogio_fisico
    variacao = random.uniform(-1.0, 1.0)
    relogio_fisico += variacao
    if relogio_fisico < 0:
        relogio_fisico = 0
    return round(relogio_fisico, 3)

def set_relogio_fisico(novo_valor):
    """
    Define o valor do relógio físico (após sincronização).
    """
    global relogio_fisico
    relogio_fisico = novo_valor

# ========== RELÓGIO LÓGICO DE LAMPORT ==========
relogio_lamport = 0

def get_relogio_lamport():
    return relogio_lamport

def incrementar_lamport():
    """
    Incrementa o relógio lógico localmente (evento interno).
    """
    global relogio_lamport
    relogio_lamport += 1
    return relogio_lamport

def atualizar_lamport(recebido):
    """
    Atualiza o relógio lógico com base em um valor recebido (evento de mensagem).
    """
    global relogio_lamport
    relogio_lamport = max(relogio_lamport, recebido) + 1
    return relogio_lamport
