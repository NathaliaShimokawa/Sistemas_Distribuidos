import json
import os

ARQUIVO_MENSAGENS = 'mensagens.json'

def carregar_mensagens():
    if os.path.exists(ARQUIVO_MENSAGENS):
        with open(ARQUIVO_MENSAGENS, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def salvar_mensagens(lista):
    with open(ARQUIVO_MENSAGENS, 'w', encoding='utf-8') as f:
        json.dump(lista, f, ensure_ascii=False, indent=2)

def adicionar_mensagem(from_, to, conteudo, logico):
    mensagens = carregar_mensagens()
    nova_mensagem = {
        "from": from_,
        "to": to,
        "conteudo": conteudo,
        "timestamp_logico": logico
    }
    mensagens.append(nova_mensagem)
    salvar_mensagens(mensagens)
    print(f"Mensagem de {from_} para {to} salva.")
