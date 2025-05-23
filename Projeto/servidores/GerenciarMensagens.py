import json
import os
from collections import defaultdict

ARQUIVO_CONVERSAS = 'conversas_formatadas.json'

def carregar_conversas():
    if os.path.exists(ARQUIVO_CONVERSAS):
        with open(ARQUIVO_CONVERSAS, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def salvar_conversas(conversas):
    with open(ARQUIVO_CONVERSAS, 'w', encoding='utf-8') as f:
        json.dump(conversas, f, ensure_ascii=False, indent=2)

def adicionar_mensagem(from_, to, conteudo, logico):
    conversas = carregar_conversas()

    chave = '|'.join(sorted([from_, to]))  # garante "ana|joao" igual a "joao|ana"

    if chave not in conversas:
        conversas[chave] = []

    nova_mensagem = {
        "from": from_,
        "to": to,
        "conteudo": conteudo,
        "timestamp_logico": logico
    }

    conversas[chave].append(nova_mensagem)
    salvar_conversas(conversas)
    print(f"Mensagem de {from_} para {to} salva na conversa {chave}.")
