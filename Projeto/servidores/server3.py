import grpc
from concurrent import futures
import time
import threading
from datetime import datetime
import random
import os, json

from GerenciarArquivo import adicionar_postagem

import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))  # Importações locais

import redesocial_pb2
import redesocial_pb2_grpc
from clock import get_relogio_fisico

# ========== CONFIGURAÇÕES ==========
SERVER_ID = "server3"
PORT = 50053
LOG_FILE = f"../logs/{SERVER_ID}.log"

# ========== ESTADO ==========
usuarios = {}
seguidores = {}
postagens = []
mensagens = []
relogio_lamport = 0
relogio_fisico = get_relogio_fisico()

lock = threading.Lock()

# ========== FUNÇÕES AUXILIARES ==========
def escrever_log(msg):
    now = datetime.now().strftime("%H:%M:%S")
    linha = f"[{now}] [Lamport: {relogio_lamport}] {msg}"
    print(linha)
    with open(LOG_FILE, "a") as f:
        f.write(linha + "\n")

def atualizar_lamport(recebido):
    global relogio_lamport
    with lock:
        relogio_lamport = max(relogio_lamport, recebido) + 1

# ========== CLASSE DO SERVIDOR ==========
class RedeSocialServicer(redesocial_pb2_grpc.RedeSocialServicer):

    def Postar(self, request, context):
        print("Recebido:", request.conteudo)
        
        try:
            conteudo_dict = json.loads(request.conteudo)
            adicionar_postagem(conteudo_dict["user_id"],conteudo_dict["conteudo"])
        except json.JSONDecodeError as e:
            escrever_log(f"Erro ao decodificar JSON: {str(e)}")
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("Conteúdo em formato inválido")
            return redesocial_pb2.Ack(message="Erro no conteúdo")

        atualizar_lamport(request.timestamp_logico)
        postagens.append({
            "conteudo": conteudo_dict
        })

        escrever_log(f'{conteudo_dict["user_id"]} postou: {conteudo_dict["conteudo"]}')
        return redesocial_pb2.Ack(message="Postagem recebida")


    def Seguir(self, request, context):
        print("Recebido:", request)
        print("Campos:", request.seguidor_id, request.seguido_id)
        atualizar_lamport(relogio_lamport)
        seguidores.setdefault(request.seguido_id, []).append(request.seguidor_id)
        escrever_log(f"{request.seguidor_id} agora segue {request.seguido_id}")
        return redesocial_pb2.Ack(message="Seguindo com sucesso")

    def EnviarMensagem(self, request, context):
        atualizar_lamport(request.timestamp_logico)
        mensagens.append({
            "from": request.from_,
            "to": request.to,
            "conteudo": request.conteudo,
            "logico": request.timestamp_logico
        })
        escrever_log(f"{request.from_} → {request.to}: {request.conteudo}")
        return redesocial_pb2.Ack(message="Mensagem enviada")

    def SincronizarRelogio(self, request, context):
        global relogio_fisico
        local = get_relogio_fisico()
        offset = local - request.relogio_fisico
        escrever_log(f"Sincronização recebida do coordenador. Offset = {offset}ms")
        return redesocial_pb2.ClockReply(offset=offset)

# ========== INICIAR SERVIDOR ==========
def serve():
    global relogio_fisico
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    redesocial_pb2_grpc.add_RedeSocialServicer_to_server(RedeSocialServicer(), server)
    server.add_insecure_port(f"[::]:{PORT}")
    server.start()
    escrever_log(f"Servidor iniciado na porta {PORT}")

    try:
        while True:
            time.sleep(5)
            relogio_fisico = get_relogio_fisico()  # Atualiza relógio físico com variação
    except KeyboardInterrupt:
        escrever_log("Servidor encerrado.")
        server.stop(0)

if __name__ == "__main__":
    os.makedirs("../logs", exist_ok=True)
    serve()
