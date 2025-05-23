const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');
const path = require('path');

const PROTO_PATH = path.join(__dirname, '..', 'servidores','redesocial.proto');

const packageDef = protoLoader.loadSync(PROTO_PATH, {
  keepCase: true,               // <- importante!
  longs: String,
  enums: String,
  defaults: true,
  oneofs: true
});

const grpcObject = grpc.loadPackageDefinition(packageDef);
const redeSocial = grpcObject.redesocial;

const client = new redeSocial.RedeSocial('localhost:50053', grpc.credentials.createInsecure());

const args = process.argv.slice(2);
const comando = args[0];
switch (comando) {
  case 'postar': {
    const [_, userId, ...conteudoArr] = args;
    const conteudo = conteudoArr.join(' ');

    if (!userId || !conteudo) {
      console.log('Uso: node User.js postar <userId> <conteudo>');
      break;
    }

    const relogioLogico = Math.floor(Math.random() * 100);
    const relogioFisico = Date.now();

    // Conteúdo como JSON em string
    const conteudoJsonString = JSON.stringify({
      user_id: userId,
      conteudo: conteudo
    });

    client.Postar({
      user_id: userId,
      conteudo: conteudoJsonString,
      timestamp_logico: relogioLogico,
      timestamp_fisico: relogioFisico
    }, (err, response) => {
      if (err) {
        console.error('Erro ao postar:', err.message);
        return;
      }
      console.log(`${userId} postou com sucesso.`);
    });
    break;
  }
    case 'enviar': {
    const [, from, to, ...conteudoArr] = args;
    const conteudo = conteudoArr.join(' ');

    if (!from || !to || !conteudo) {
      console.log('Uso: node User.js enviarMensagem <de> <para> <conteudo>');
      break;
    }

    const relogioLogico = Math.floor(Math.random() * 100);

    client.EnviarMensagem({
      from_: from,
      to: to,
      conteudo: conteudo,
      timestamp_logico: relogioLogico
    }, (err, res) => {
      if (err) {
        console.error('Erro ao enviar mensagem:', err.message);
        return;
      }
      console.log(`Mensagem enviada de ${from} para ${to}.`);
    });
    break;
  }
  case 'seguir': {
    const [, seguidorid, seguidoid] = args;

    if (!seguidorid || !seguidoid) {
      console.log('Uso: node User.js seguir <seguidorid> <seguidoid>');
      break;
    }

    client.Seguir({ seguidoid,seguidorid}, (err, res) => {
      if (err) {
        console.error('Erro ao seguir:', err.message);
        return;
      }
      console.log(`${seguidorid} agora segue ${seguidoid}.`);
    });
    break;
  }

  default:
    console.log('Comando inválido.');
    console.log('Uso:');
    console.log('  node User.js postar <userId> <conteudo>');
    console.log('  node User.js seguir <seguidorId> <seguidoId>');
}