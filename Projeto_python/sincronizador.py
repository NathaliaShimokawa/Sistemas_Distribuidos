import threading
import time
from datetime import datetime

class Sincronizador:
    def __init__(self, servidores):
        self.servidores = servidores  # dicionário {nome: servidor}
        self.coordenador = None
        self.sync_interval = 20  # segundos

        t = threading.Thread(target=self.executar_periodicamente)
        t.daemon = True
        t.start()

    def log(self, msg):
        print(f"[SYNC] {datetime.now().strftime('%H:%M:%S')} - {msg}")

    def eleger_coordenador(self):
        nomes = list(self.servidores.keys())
        eleito = max(nomes)  # maior nome vence (simulando ID)
        self.coordenador = self.servidores[eleito]
        self.log(f"Coordenador eleito: {eleito}")
        return self.coordenador

    def sincronizar_berkeley(self):
        if not self.coordenador:
            self.eleger_coordenador()

        coordenador_nome = self.coordenador.nome
        tempos = {}
        media_segundos = 0

        # Passo 1: Coordenador coleta tempos
        for nome, servidor in self.servidores.items():
            tempo = servidor.get_tempo_fisico()
            delta = (tempo - self.coordenador.get_tempo_fisico()).total_seconds()
            tempos[nome] = delta
            media_segundos += delta

        media_segundos /= len(tempos)

        # Passo 2: Envia ajustes para cada servidor
        for nome, servidor in self.servidores.items():
            ajuste = media_segundos - tempos[nome]
            servidor.ajustar_relogio_fisico(ajuste)

        self.log(f"Sincronização realizada. Coordenador: {coordenador_nome}. Média: {media_segundos:.3f}s")
        for nome in tempos:
            self.log(f"Ajuste enviado para {nome}: {(media_segundos - tempos[nome]):.3f}s")

    def executar_periodicamente(self):
        while True:
            time.sleep(self.sync_interval)
            self.eleger_coordenador()
            self.sincronizar_berkeley()
