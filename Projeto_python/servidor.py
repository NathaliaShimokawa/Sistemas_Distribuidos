import threading
import random
import time
from relogio import Relogio
from datetime import datetime
import os

class Servidor:
    def __init__(self, nome, rede_servidores):
        self.nome = nome
        self.relogio = Relogio(nome)
        self.rede_servidores = rede_servidores  # lista de servidores (referência cruzada)
        self.posts = []  # (autor, conteudo, timestamp)
        self.mensagens = []  # (de, para, conteudo, timestamp)
        self.lock = threading.Lock()
        self.log_file = open(f"logs/{self.nome}.log", "a")

        self.ativo = True
        self.rede_servidores[nome] = self

        self.log(f"Servidor {self.nome} iniciado")

    def log(self, msg):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        entrada = f"[{timestamp}] {msg}"
        self.log_file.write(entrada + "\n")
        self.log_file.flush()
        print(f"[{self.nome}] {msg}")

    def receber_post(self, autor, conteudo, ts):
        with self.lock:
            self.relogio.receber_timestamp(ts)
            self.posts.append((autor, conteudo, ts))
            self.log(f"POST recebido de {autor}: '{conteudo}' | ts lógico: {ts}")
            self.replicar_post(autor, conteudo, ts)

    def receber_mensagem(self, de_usuario, para_usuario, conteudo, ts):
        with self.lock:
            self.relogio.receber_timestamp(ts)
            self.mensagens.append((de_usuario, para_usuario, conteudo, ts))
            self.log(f"MENSAGEM recebida de {de_usuario} para {para_usuario}: '{conteudo}' | ts lógico: {ts}")
            self.replicar_mensagem(de_usuario, para_usuario, conteudo, ts)

    # replica os posts para os outros servidores
    def replicar_post(self, autor, conteudo, ts):
        for nome, servidor in self.rede_servidores.items():
            if nome != self.nome:
                servidor.replica_recebida_post(autor, conteudo, ts)

    # replica as mensagens para os outros servidores
    def replicar_mensagem(self, de_usuario, para_usuario, conteudo, ts):
        for nome, servidor in self.rede_servidores.items():
            if nome != self.nome:
                servidor.replica_recebida_mensagem(de_usuario, para_usuario, conteudo, ts)

    def replica_recebida_post(self, autor, conteudo, ts):
        with self.lock:
            self.posts.append((autor, conteudo, ts))
            self.log(f"[REPLICA] POST de {autor} armazenado | ts: {ts}")

    def replica_recebida_mensagem(self, de_usuario, para_usuario, conteudo, ts):
        with self.lock:
            self.mensagens.append((de_usuario, para_usuario, conteudo, ts))
            self.log(f"[REPLICA] MENSAGEM de {de_usuario} para {para_usuario} armazenada | ts: {ts}")

    def get_tempo_fisico(self):
        return self.relogio.hora_fisica()

    def ajustar_relogio_fisico(self, delta_s):
        self.relogio.ajustar_fisico(delta_s)
        self.log(f"[SYNC] Ajuste de relógio físico: {delta_s:.3f}s")
