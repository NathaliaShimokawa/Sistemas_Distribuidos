import json
import os

ARQUIVO_SEGUIDORES = 'seguidores.json'

def carregar_seguidores():
    if os.path.exists(ARQUIVO_SEGUIDORES):
        with open(ARQUIVO_SEGUIDORES, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def salvar_seguidores(data):
    with open(ARQUIVO_SEGUIDORES, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def adicionar_seguidor(seguido_id, seguidor_id):

    data = carregar_seguidores()

    if seguido_id not in data:
        data[seguido_id] = []

    if seguidor_id not in data[seguido_id]:
        data[seguido_id].append(seguidor_id)

    salvar_seguidores(data)
    print(f"{seguidor_id} agora segue {seguido_id}.")
