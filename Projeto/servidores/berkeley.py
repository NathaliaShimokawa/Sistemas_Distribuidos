import grpc
import time
import threading
from datetime import datetime
import random
import os

import redesocial_pb2
import redesocial_pb2_grpc
from clock import get_relogio_fisico, set_relogio_fisico

COORDINADOR = "server1"
SERVIDORES = ["server1", "server2", "server3"]
PORT = 50053  

relogio_fisico = get_relogio_fisico()
offsets = {}

def escrever_log(msg):
    now = datetime.now().strftime("%H:%M:%S")
    linha = f"[{now}] {msg}"
    print(linha)

def sincronizar_com_servidores():
    """
    Função que sincroniza os relógios de todos os servidores com o coordenador.
    O coordenador envia um offset para os servidores ajustarem seus relógios.
    """
    global relogio_fisico

    for servidor in SERVIDORES:
        if servidor == COORDINADOR:
            continue 

        try:
            channel = grpc.insecure_channel(f'localhost:{50051 if servidor == "server1" else 50052}')
            stub = redesocial_pb2_grpc.RedeSocialStub(channel)

            response = stub.SincronizarRelogio(redesocial_pb2.ClockRequest(relogio_fisico=relogio_fisico))
            offset = response.offset

            offsets[servidor] = offset
            escrever_log(f"Servidor {servidor} sincronizado. Offset: {offset}ms")

            novo_relogio = get_relogio_fisico() + offset
            set_relogio_fisico(novo_relogio)

        except grpc.RpcError as e:
            escrever_log(f"Erro ao sincronizar com o servidor {servidor}: {e}")

def serve():
    """
    Inicia o coordenador, que vai fornecer os offsets para os servidores.
    """
    global relogio_fisico
    escrever_log(f"Coordenador iniciado (Servidor {COORDINADOR})")

    while True:
        try:
            time.sleep(10)
            sincronizar_com_servidores()

        except KeyboardInterrupt:
            escrever_log("Coordenador interrompido.")
            break

if __name__ == "__main__":
    os.makedirs("../logs", exist_ok=True)
    serve()
