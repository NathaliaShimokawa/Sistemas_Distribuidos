import grpc
from concurrent import futures
import time
import threading
from datetime import datetime
import random
import os, json

from GerenciarMensagens import adicionar_mensagem
from GerenciarSeguidores import adicionar_seguidor
from GerenciarArquivo import adicionar_postagem

import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__))) 

import redesocial_pb2
import redesocial_pb2_grpc
from clock import get_relogio_fisico


SERVER_ID = "server3"
PORT = 50053
LOG_FILE = f"../logs/{SERVER_ID}.log"


usuarios = {}
seguidores = {}
postagens = []
mensagens = []
relogio_lamport = 0
relogio_fisico = get_relogio_fisico()

lock = threading.Lock()


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
clientes_streams = {}

class RedeSocialServicer(redesocial_pb2_grpc.RedeSocialServicer):

    def Postar(self, request, context):
        print("Recebido:", request.conteudo)
        
        try:
            conteudo_dict = json.loads(request.conteudo)
            user_id = conteudo_dict["user_id"]
            texto = conteudo_dict["conteudo"]
            adicionar_postagem(user_id, texto)
        except json.JSONDecodeError as e:
            escrever_log(f"Erro ao decodificar JSON: {str(e)}")
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("Conteúdo em formato inválido")
            return redesocial_pb2.Ack(message="Erro no conteúdo")

        atualizar_lamport(request.timestamp_logico)

        postagem = redesocial_pb2.Postagem(
            user_id=user_id,
            conteudo=texto,
            timestamp_logico=request.timestamp_logico,
            timestamp_fisico=request.timestamp_fisico,
        )

        seguidores_do_user = seguidores.get(user_id, [])
        for seguidor_id in seguidores_do_user:
            for cliente_context in clientes_streams.get(seguidor_id, []):
                try:
                    cliente_context.send_message(postagem)
                except Exception as e:
                    print(f"Erro ao enviar para {seguidor_id}: {e}")

        escrever_log(f'{user_id} postou: {texto}')
        return redesocial_pb2.Ack(message="Postagem recebida")



    def Seguir(self, request, context):
        print("Recebido:", request)
        print("Campos:", request.seguidorid, request.seguidoid)

        atualizar_lamport(relogio_lamport)
        
        adicionar_seguidor(request.seguidoid, request.seguidorid)

        escrever_log(f"{request.seguidorid} agora segue {request.seguidoid}")
        return redesocial_pb2.Ack(message="Seguindo com sucesso")


    def EnviarMensagem(self, request, context):
        print("Recebido:", request)

        atualizar_lamport(request.timestamp_logico)

        adicionar_mensagem(
            from_=request.from_,
            to=request.to,
            conteudo=request.conteudo,
            logico=request.timestamp_logico
        )

        escrever_log(f"{request.from_} enviou mensagem para {request.to}: {request.conteudo}")
        return redesocial_pb2.Ack(message="Mensagem enviada")
    
    def ReceberPostagens(self, request, context):
        user_id = request.user_id
        print(f"Usuário conectado para receber postagens: {user_id}")

        from queue import Queue
        fila = Queue()
        self.usuarios_conectados[user_id] = fila

        try:
            while True:
                postagem = fila.get() 
                yield postagem 
        except Exception as e:
            print(f"Erro no stream do usuário {user_id}: {e}")
        finally:
            print(f"Stream encerrado para {user_id}")
            del self.usuarios_conectados[user_id]


    def SincronizarRelogio(self, request, context):
        global relogio_fisico
        local = get_relogio_fisico()
        offset = local - request.relogio_fisico
        escrever_log(f"Sincronização recebida do coordenador. Offset = {offset}ms")
        return redesocial_pb2.ClockReply(offset=offset)

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
            relogio_fisico = get_relogio_fisico() 
    except KeyboardInterrupt:
        escrever_log("Servidor encerrado.")
        server.stop(0)

if __name__ == "__main__":
    os.makedirs("../logs", exist_ok=True)
    serve()