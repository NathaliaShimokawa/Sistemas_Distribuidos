# Projeto Sistemas Distribuídos

# 🖥️ Sistema Distribuído com gRPC

Este projeto implementa um sistema distribuído no qual múltiplos servidores e clientes se comunicam via gRPC. O coordenador Berkeley é responsável por orquestrar o algoritmo de sincronização de relógios, garantindo que todos os servidores estejam sincronizados.

## Arquitetura

- **Servidores** (Python): 3 instâncias que participam da sincronização de relógios.
- **Cliente Go**: Cliente implementado em **Go**.
- **Cliente JavaScript**: Cliente implementado em **Node.js**.
- **Coordenador Berkeley** (Python): Responsável por coletar offsets e ajustar os relógios dos servidores.

##  Como executar

### Inicie os servidores

Em terminais separados, execute os seguintes comandos dentro da pasta `servidores`: <br>
python server1.py <br>
python server2.py <br>
python server3.py <br>


### Inicie o Coordenador Berkeley

Em outro terminal, dentro da pasta servidores, execute: <br>
python berkeley.py


### Execute os Clientes

Para executar o cliente Go (na pasta raiz do projeto): <br>
go run User.go <br><br>

Para executar o cliente JavaScript (dentro da pasta clientes): <br>
node User.js <br><br>


## Diagrama:
![RedesSocias drawio](https://github.com/user-attachments/assets/82f40770-e375-4d94-abde-014f7aeb830b)


## Desenvolvido por:
*Lucas Sombra do Nascimento (22.122.112-0)* <br>
*Nathalia Saori Shimokawa (22.122.052-8)*
