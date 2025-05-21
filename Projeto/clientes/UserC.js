const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');
const path = require('path');

// Caminho correto para acessar o .proto a partir da pasta "clientes"
const PROTO_PATH = path.join(__dirname, '..', 'redesocial.proto');

// Carregar definições do .proto
const packageDef = protoLoader.loadSync(PROTO_PATH);
const grpcObject = grpc.loadPackageDefinition(packageDef);

// Corrigir o nome do pacote para 'redesocial'
const redeSocial = grpcObject.redesocial;  // Altere para 'redesocial'

// Criar cliente
const client = new redeSocial.RedeSocial('localhost:50053', grpc.credentials.createInsecure());

// Dados do usuário
const userId = "UserC";
const relogioLogico = Math.floor(Math.random() * 100);
const relogioFisico = Date.now() / 1000;

// Fazer postagem
client.Postar({
  user_id: userId,
  conteudo: "Olá! Aqui é o UserC.",
  timestamp_logico: relogioLogico,
  timestamp_fisico: relogioFisico
}, (err, response) => {
  if (err) {
    console.error("Erro ao postar:", err.message);
    return;
  }
  console.log("UserC postou.");

  // Seguir outro usuário
  client.Seguir({
    seguidor_id: userId,
    seguido_id: "UserD"
  }, (err, res) => {
    if (err) {
      console.error("Erro ao seguir:", err.message);
      return;
    }
    console.log("UserC agora segue UserD.");
  });
});
