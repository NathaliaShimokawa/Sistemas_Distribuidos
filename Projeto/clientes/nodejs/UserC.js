const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');
const path = require('path');

const packageDef = protoLoader.loadSync(
  path.resolve(__dirname, '../../proto/redesocial.proto')
);
const grpcObject = grpc.loadPackageDefinition(packageDef);
const redeSocial = grpcObject.redeSocial;

const client = new redeSocial.RedeSocial('localhost:50053', grpc.credentials.createInsecure());

const userId = "UserC";
const relogioLogico = Math.floor(Math.random() * 100);
const relogioFisico = (Date.now() / 1000).toFixed(3);

client.Postar({
  user_id: userId,
  conteudo: "Olá! Aqui é o UserC.",
  timestamp_logico: relogioLogico,
  timestamp_fisico: relogioFisico
}, (err, response) => {
  if (!err) {
    console.log("UserC postou.");
  }

  client.Seguir({
    seguidor_id: userId,
    seguido_id: "UserD"
  }, (err, res) => {
    if (!err) {
      console.log("UserC agora segue UserD.");
    }
  });
});
