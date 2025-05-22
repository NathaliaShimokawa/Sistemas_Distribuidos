const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');
const path = require('path');
const fs = require('fs');

// Caminho do .proto
const PROTO_PATH = path.join(__dirname, '..', 'redesocial.proto');

// Carrega o .proto
const packageDef = protoLoader.loadSync(PROTO_PATH);
const grpcObject = grpc.loadPackageDefinition(packageDef);
const redeSocial = grpcObject.redesocial;

// Cria cliente
const client = new redeSocial.RedeSocial('localhost:50053', grpc.credentials.createInsecure());

// Caminhos dos arquivos JSON
const MENSAGENS_JSON = path.join(__dirname, 'mensagens.json');
const SEGUIDORES_JSON = path.join(__dirname, 'seguidores.json');
const POSTAGENS_JSON = path.join(__dirname, 'postagens.json');

// Função para salvar em JSON
function salvarJSON(caminho, dados) {
  fs.writeFileSync(caminho, JSON.stringify(dados, null, 2), 'utf-8');
}

// Carregar dados do JSON
function carregarJSON(caminho) {
  if (!fs.existsSync(caminho)) return [];
  return JSON.parse(fs.readFileSync(caminho, 'utf-8'));
}

// Lê argumentos da linha de comando
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

  case 'seguir': {
    const [_, seguidorId, seguidoId] = args;
    if (!seguidorId || !seguidoId) {
      console.log('Uso: node User.js seguir <seguidorId> <seguidoId>');
      break;
    }

    const relogioLogico = Math.floor(Math.random() * 100);

    client.Seguir({
      seguidor_id: seguidorId,
      seguido_id: seguidoId,
      timestamp_logico: relogioLogico
    }, (err, res) => {
      if (err) {
        console.error('Erro ao seguir:', err.message);
        return;
      }
      console.log(`${seguidorId} agora segue ${seguidoId}.`);

      // Persistir em seguidores.json
      const dadosSeguidores = carregarJSON(SEGUIDORES_JSON);
      dadosSeguidores.push({
        seguidor_id: seguidorId,
        seguido_id: seguidoId,
        timestamp_logico: relogioLogico,
        timestamp: new Date().toISOString()
      });
      salvarJSON(SEGUIDORES_JSON, dadosSeguidores);
    });
    break;
  }

  case 'enviarMensagem': {
  const [_, de, para, ...mensagemArr] = args;
  const conteudo = mensagemArr.join(' ');

  if (!de || !para || !conteudo) {
    console.log('Uso: node User.js enviarMensagem <de> <para> <mensagem>');
    break;
  }

  const relogioLogico = Math.floor(Math.random() * 100);

  client.EnviarMensagem({
    from_: de,
    to: para,
    conteudo: conteudo,
    timestamp_logico: relogioLogico
  }, (err, res) => {
    if (err) {
      console.error('Erro ao enviar mensagem:', err.message);
      return;
    }
    console.log(`${de} enviou mensagem para ${para}: "${conteudo}"`);
    console.log(`Resposta do servidor: ${res.message}`);
  });

  break;
}


  default:
    console.log('Comando inválido.');
    console.log('Uso:');
    console.log('  node User.js postar <userId> <conteudo>');
    console.log('  node User.js seguir <seguidorId> <seguidoId>');
    console.log('  node User.js enviarMensagem <de> <para> <mensagem>');
}
