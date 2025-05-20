import time
import random

# Variável global para o relógio físico
relogio_fisico = 0

def get_relogio_fisico():
    """
    Retorna o valor do relógio físico com uma variação aleatória de até 1 segundo.
    Isso simula o comportamento de um relógio físico que pode atrasar ou adiantar aleatoriamente.
    """
    global relogio_fisico

    # Variação aleatória entre -1s e +1s
    variacao = random.uniform(-1.0, 1.0)
    relogio_fisico += variacao

    # Garante que o relógio não tenha valores negativos
    if relogio_fisico < 0:
        relogio_fisico = 0
    
    return round(relogio_fisico, 3)  # Arredonda para 3 casas decimais

def set_relogio_fisico(novo_relogio):
    """
    Define manualmente o valor do relógio físico. Usado em casos de sincronização.
    """
    global relogio_fisico
    relogio_fisico = novo_relogio
