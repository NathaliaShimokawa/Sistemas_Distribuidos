const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');
const path = require('path');

const packageDef = protoLoader.loadSync(
  path.resolve(__dirname, '../../proto/redesocial.proto')
);
const grpcObject = grpc.loadPackageDefinition(packageDef);
const redeSocial = grpcObject.redeSocial;

const client = new redeSocial.RedeSocial('localhost:50051', grpc.credentials.createInsecure());

const userId = "UserD";
const relogioLogico = Math.floor(Math.random() * 100);
const relogioFisico = (Date.now() / 1000).toFixed(3);

client.Postar({
  user_id: userId,
  conteudo: "Mensagem pública do UserD.",
  timestamp_logico: relogioLogico,
  timestamp_fisico: relogioFisico
}, (err, response) => {
  if (!err) {
    console.log("UserD postou.");
  }

  client.EnviarMensagem({
    from: userId,
    to: "UserE",
    conteudo: "Olá UserE!",
    timestamp_logico: relogioLogico + 1
  }, (err, res) => {
    if (!err) {
      console.log("UserD enviou mensagem para UserE.");
    }
  });
});
