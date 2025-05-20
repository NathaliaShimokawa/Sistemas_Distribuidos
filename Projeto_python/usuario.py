import threading
import random
import time
from relogio import Relogio
from comunicacao import enviar_post, enviar_mensagem
from datetime import datetime

class Usuario:
    def __init__(self, nome, automatico=False, intervalo_acao=(3, 8)):
        self.nome = nome
        self.relogio = Relogio(nome)
        self.automatico = automatico
        self.intervalo_acao = intervalo_acao
        self.log_file = open(f"logs/{self.nome}.log", "a")

        self.seguindo = set()
        self.start()

    def start(self):
        if self.automatico:
            t = threading.Thread(target=self.executar_automaticamente)
            t.daemon = True
            t.start()

    def executar_automaticamente(self):
        while True:
            acao = random.choice(["postar", "mensagem"])
            if acao == "postar":
                self.postar(f"Post automático de {self.nome}")
            else:
                destino = f"user{random.randint(1, 5)}"
                if destino != self.nome:
                    self.enviar_mensagem(destino, f"Olá {destino}! - de {self.nome}")
            time.sleep(random.randint(*self.intervalo_acao))

    def log(self, msg):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] {msg}\n"
        self.log_file.write(log_entry)
        self.log_file.flush()
        print(f"[{self.nome}] {msg}")

    def postar(self, conteudo):
        ts = self.relogio.tick_logico()
        enviar_post(self.nome, conteudo, ts)
        self.log(f"POST: '{conteudo}' | ts lógico: {ts}")

    def enviar_mensagem(self, destinatario, conteudo):
        ts = self.relogio.tick_logico()
        enviar_mensagem(self.nome, destinatario, conteudo, ts)
        self.log(f"MENSAGEM: para {destinatario}: '{conteudo}' | ts lógico: {ts}")

    def receber_mensagem(self, remetente, conteudo, ts_remoto):
        ts_local = self.relogio.receber_timestamp(ts_remoto)
        self.log(f"MENSAGEM RECEBIDA de {remetente}: '{conteudo}' | ts lógico atualizado: {ts_local}")

    def receber_post(self, autor, conteudo, ts_remoto):
        ts_local = self.relogio.receber_timestamp(ts_remoto)
        self.log(f"POST RECEBIDO de {autor}: '{conteudo}' | ts lógico atualizado: {ts_local}")

    def seguir(self, outro_usuario):
        self.seguindo.add(outro_usuario)
        self.log(f"SEGUINDO: {outro_usuario}")
