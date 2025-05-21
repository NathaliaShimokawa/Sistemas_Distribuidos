const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');
const path = require('path');

const packageDef = protoLoader.loadSync(
  path.resolve(__dirname, '../../proto/redesocial.proto')
);
const grpcObject = grpc.loadPackageDefinition(packageDef);
const redeSocial = grpcObject.redeSocial;

const client = new redeSocial.RedeSocial('localhost:50052', grpc.credentials.createInsecure());

const userId = "UserE";
const relogioLogico = Math.floor(Math.random() * 100);
const relogioFisico = (Date.now() / 1000).toFixed(3);

client.Postar({
  user_id: userId,
  conteudo: "Post do UserE.",
  timestamp_logico: relogioLogico,
  timestamp_fisico: relogioFisico
}, (err, response) => {
  if (!err) {
    console.log("UserE postou.");
  }

  client.EnviarMensagem({
    from: userId,
    to: "UserC",
    conteudo: "Oi UserC!",
    timestamp_logico: relogioLogico + 2
  }, (err, res) => {
    if (!err) {
      console.log("UserE enviou mensagem para UserC.");
    }
  });
});
