# Sistemas_Distribuidos

![RedesSocias drawio](https://github.com/user-attachments/assets/82f40770-e375-4d94-abde-014f7aeb830b)
# Documentação do Projeto - Sistema Distribuído de Rede Social

## Padrão de Mensagens gRPC

Este projeto utiliza o protocolo **gRPC** com mensagens definidas no arquivo `redesocial.proto`, que padroniza a comunicação entre cliente e servidor. Abaixo estão descritas todas as mensagens e serviços utilizados no projeto.

---

## Serviços e Mensagens

### 1. Postagem

**Serviço:** `Postar`

```proto
message PostagemRequest {
  string user_id = 1;
  string conteudo = 2;
  int32 timestamp_logico = 3;
  int64 timestamp_fisico = 4;
}
```

**Descrição:**  
Permite que um usuário poste uma mensagem. A postagem inclui informações sobre o autor, o conteúdo, um timestamp lógico (Lamport) e um timestamp físico (em milissegundos). O servidor notifica os seguidores conectados em tempo real.

---

### 2. Seguir Usuário

**Serviço:** `Seguir`

```proto
message SeguirRequest {
  string seguidoid = 1;
  string seguidorid = 2;
  int32 relogioLogico = 3;
}
```

**Descrição:**  
Permite que um usuário siga outro. A relação é armazenada no servidor para envio de notificações futuras.

---

### 3. Mensagens Diretas

**Serviço:** `EnviarMensagem`

```proto
message MensagemRequest {
  string from = 1;
  string to = 2;
  string conteudo = 3;
  int32 timestamp_logico = 4;
}
```

**Descrição:**  
Permite que um usuário envie mensagens diretas para outro. Essas mensagens são salvas em arquivos para persistência e podem ser visualizadas a qualquer momento.

---

### 4. Notificação de Postagem

**Serviço:** `ReceberPostagens` *(gRPC Streaming)*

```proto
message ReceberRequest {
  string user_id = 1;
}
```

**Descrição:**  
Método de streaming que permite que o servidor envie notificações em tempo real para usuários que seguem outros. Quando um usuário que você segue posta algo, você recebe automaticamente a postagem no console.

---

### 5. Sincronização de Relógio

**Serviço:** `SincronizarRelogio`

```proto
message ClockRequest {
  double relogio_fisico = 1;
}

message ClockReply {
  double offset = 1;
}
```

**Descrição:**  
Utilizado para sincronizar o relógio físico dos servidores usando o algoritmo de Berkeley. Um servidor coordenador solicita os relógios dos demais e calcula um offset para alinhamento.

---

### 6. Ack (Confirmação)

```proto
message Ack {
  string message = 1;
}
```

**Descrição:**  
Mensagem de confirmação genérica retornada após a execução de serviços como postagem, envio de mensagens e seguir usuários.
