import os
import time
from servidor import Servidor
from usuario import Usuario
from comunicacao import registrar_usuario
from sincronizador import Sincronizador

# Garantir pasta de logs
os.makedirs("logs", exist_ok=True)

# === Inicialização da Rede de Servidores ===
rede_servidores = {}

servidorA = Servidor("servidorA", rede_servidores)
servidorB = Servidor("servidorB", rede_servidores)
servidorC = Servidor("servidorC", rede_servidores)

servidores = [servidorA, servidorB, servidorC]

# === Inicialização de Usuários ===
usuarios = []

usuario1 = Usuario("user1", automatico=True)
usuario2 = Usuario("user2", automatico=True)
usuario3 = Usuario("user3", automatico=True)
usuario4 = Usuario("user4", automatico=False)
usuario5 = Usuario("user5", automatico=False)

usuarios.extend([usuario1, usuario2, usuario3, usuario4, usuario5])

# === Registrar usuários na rede de comunicação ===
for user in usuarios:
    registrar_usuario(user)

# === Seguir usuários (simples predefinição) ===
usuario4.seguir("user1")
usuario4.seguir("user2")
usuario5.seguir("user3")

# === Iniciar Sincronizador de Relógios ===
sincronizador = Sincronizador(rede_servidores)

# === Simular entrada de dados manuais (usuários não automáticos) ===
def entrada_manual():
    while True:
        print("\n--- Ações disponíveis ---")
        print("1. Postar")
        print("2. Enviar mensagem")
        print("3. Sair")

        escolha = input("Escolha (1/2/3): ")
        if escolha == "1":
            nome = input("Usuário: ")
            conteudo = input("Conteúdo do post: ")
            for user in usuarios:
                if user.nome == nome:
                    user.postar(conteudo)
        elif escolha == "2":
            nome = input("Remetente: ")
            destinatario = input("Destinatário: ")
            conteudo = input("Mensagem: ")
            for user in usuarios:
                if user.nome == nome:
                    user.enviar_mensagem(destinatario, conteudo)
        elif escolha == "3":
            print("Encerrando entrada manual.")
            break
        else:
            print("Opção inválida.")

# Rodar entrada manual em thread separada
import threading
entrada_thread = threading.Thread(target=entrada_manual)
entrada_thread.start()

# Sistema permanece ativo
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nEncerrando sistema...")
