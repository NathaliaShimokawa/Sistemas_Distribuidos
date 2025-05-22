const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');
const path = require('path');

// Caminho correto para acessar o .proto a partir da pasta "clientes"
const PROTO_PATH = path.join(__dirname, '..', 'redesocial.proto');

// Carregar definições do .proto
const packageDef = protoLoader.loadSync(PROTO_PATH);
const grpcObject = grpc.loadPackageDefinition(packageDef);

// Corrigir o nome do pacote para 'redesocial'
const redeSocial = grpcObject.redesocial;  // Nome correto do pacote

// Criar cliente
const client = new redeSocial.RedeSocial('localhost:50053', grpc.credentials.createInsecure()); // Certifique-se de usar a porta correta

// Dados do usuário
const userId = "UserD";
const relogioLogico = Math.floor(Math.random() * 100);
const relogioFisico = Date.now() / 1000; // Considerando timestamp em segundos

// Fazer postagem
client.Postar({
  user_id: userId,
  conteudo: "Mensagem pública do UserD.",
  timestamp_logico: relogioLogico,
  timestamp_fisico: relogioFisico
}, (err, response) => {
  if (err) {
    console.error("Erro ao postar:", err.message);
    return;
  }
  console.log("UserD postou.");

  // Enviar mensagem para UserE
  client.EnviarMensagem({
    from_: userId,  // Certifique-se de usar 'from_' como no .proto
    to: "UserE",
    conteudo: "Olá UserE!",
    timestamp_logico: relogioLogico + 1  // Incrementando o timestamp lógico
  }, (err, res) => {
    if (err) {
      console.error("Erro ao enviar mensagem:", err.message);
      return;
    }
    console.log("UserD enviou mensagem para UserE.");
  });
});
