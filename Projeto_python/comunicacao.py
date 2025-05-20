from threading import Lock
from collections import defaultdict

# simula a rede
usuarios_registrados = {}
mensagens_pendentes = defaultdict(list)
posts_publicados = defaultdict(list)
lock = Lock()

# registra o usuario, para receber posts e mensagens
def registrar_usuario(usuario):
    with lock:
        usuarios_registrados[usuario.nome] = usuario

# envia os posts para os seguidores
def enviar_post(remetente, conteudo, timestamp):
    with lock:
        posts_publicados[remetente].append((conteudo, timestamp))
        # Notificar seguidores
        for nome, usuario in usuarios_registrados.items():
            if remetente in usuario.seguindo:
                usuario.receber_post(remetente, conteudo, timestamp)

# envia a mensagem 
def enviar_mensagem(remetente, destinatario, conteudo, timestamp):
    with lock:
        if destinatario in usuarios_registrados:
            usuario_destino = usuarios_registrados[destinatario]
            usuario_destino.receber_mensagem(remetente, conteudo, timestamp)
        else:
            mensagens_pendentes[destinatario].append((remetente, conteudo, timestamp))

# quando o usuario nao esta conectado, ele guarda as mensagens e envia quando o usuario estiver conectado
def despachar_mensagens_pendentes(nome_usuario):
    with lock:
        if nome_usuario in usuarios_registrados and nome_usuario in mensagens_pendentes:
            destino = usuarios_registrados[nome_usuario]
            for remetente, conteudo, ts in mensagens_pendentes[nome_usuario]:
                destino.receber_mensagem(remetente, conteudo, ts)
            mensagens_pendentes[nome_usuario] = []
