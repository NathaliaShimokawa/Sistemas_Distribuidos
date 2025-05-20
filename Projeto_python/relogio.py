import time
import random
from datetime import datetime, timedelta

class Relogio:
    def __init__(self, nome_processo):
        self.nome = nome_processo
        self.logico = 0
        self._drift = random.uniform(-1, 1)
        self.fisico_base = datetime.now()
        self.ajuste = timedelta(seconds=0)

    # incrementa o relogio logico antes de um evento local
    def tick_logico(self):
        self.logico += 1
        return self.logico

    # ajusta o relogio logico quando recebe a mensagem
    def receber_timestamp(self, ts_remoto):
        self.logico = max(self.logico, ts_remoto) + 1
        return self.logico

    # coloca a hora atual, com o desvio 
    def hora_fisica(self):
        drift_total = self._drift + self.ajuste.total_seconds()
        return self.fisico_base + timedelta(seconds=drift_total)

    # altera o horario fisico durante a sincronizacao
    def ajustar_fisico(self, diferenca_segundos):
        self.ajuste += timedelta(seconds=diferenca_segundos)

    def __str__(self):
        return f"[{self.nome}] Logico: {self.logico}, Fisico: {self.hora_fisica().strftime('%H:%M:%S.%f')[:-3]}"
