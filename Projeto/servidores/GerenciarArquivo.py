import json
import os

ARQUIVO = 'postagens.json'

def carregar_postagens():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def salvar_postagens(data):
    with open(ARQUIVO, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def adicionar_postagem(user_id, conteudo):
    data = carregar_postagens()

    if user_id not in data:
        data[user_id] = []

    data[user_id].append(conteudo)
    salvar_postagens(data)
    print(f'Postagem adicionada para {user_id}.')

# Exemplo de uso

