const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');
const path = require('path');
const readline = require('readline');
const fs = require('fs');

const PROTO_PATH = path.join(__dirname, '..', 'servidores', 'redesocial.proto');

const packageDef = protoLoader.loadSync(PROTO_PATH, {
  keepCase: true,
  longs: String,
  enums: String,
  defaults: true,
  oneofs: true
});

const grpcObject = grpc.loadPackageDefinition(packageDef);
const redeSocial = grpcObject.redesocial;
const client = new redeSocial.RedeSocial('localhost:50053', grpc.credentials.createInsecure());

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

function prompt(question) {
  return new Promise(resolve => rl.question(question, resolve));
}

let usuarioLogado = '';

function escutarPostagens() {
  const stream = client.ReceberPostagens({ user_id: usuarioLogado });

  stream.on('data', (postagem) => {
    const dados = JSON.parse(postagem.conteudo);
    console.log(`\n🔔 Notificação: ${dados.user_id} fez uma nova postagem!`);
    console.log(`📝 "${dados.conteudo}"\n`);
  });

  stream.on('error', (err) => {
    console.error('Erro no stream de postagens:', err.message);
  });

  stream.on('end', () => {
    console.log('Stream finalizado.');
  });
}


async function menu() {
  console.log(`\n📱 Bem-vindo, ${usuarioLogado}!`);
  console.log('1 - Postar');
  console.log('2 - Enviar mensagem');
  console.log('3 - Seguir alguém');
  console.log('4 - Ver conversa com alguém');
  console.log('5 - Sair');

  const opcao = await prompt('\nEscolha uma opção: ');

  switch (opcao) {
    case '1': {
      const conteudo = await prompt('Digite o conteúdo da postagem: ');
      const relogioLogico = Math.floor(Math.random() * 100);
      const relogioFisico = Date.now();

      const conteudoJsonString = JSON.stringify({
        user_id: usuarioLogado,
        conteudo: conteudo
      });

      client.Postar({
        user_id: usuarioLogado,
        conteudo: conteudoJsonString,
        timestamp_logico: relogioLogico,
        timestamp_fisico: relogioFisico
      }, (err, response) => {
        if (err) {
          console.error('❌ Erro ao postar:', err.message);
        } else {
          console.log('✅ Postagem enviada com sucesso.');
        }
        menu();
      });
      break;
    }

    case '2': {
      const destino = await prompt('Para quem deseja enviar mensagem? ');
      const conteudo = await prompt('Digite a mensagem: ');
      const relogioLogico = Math.floor(Math.random() * 100);

      client.EnviarMensagem({
        from_: usuarioLogado,
        to: destino,
        conteudo: conteudo,
        timestamp_logico: relogioLogico
      }, (err, res) => {
        if (err) {
          console.error('❌ Erro ao enviar mensagem:', err.message);
        } else {
          console.log(`✅ Mensagem enviada para ${destino}.`);
        }
        menu();
      });
      break;
    }

    case '3': {
      const seguido = await prompt('Quem você quer seguir? ');
      const relogioLogico = Math.floor(Math.random() * 100);

      client.Seguir({
        seguidoid: seguido,
        seguidorid: usuarioLogado,
        relogioLogico
      }, (err, res) => {
        if (err) {
          console.error('❌ Erro ao seguir:', err.message);
        } else {
          console.log(`✅ Agora você segue ${seguido}.`);
        }
        menu();
      });
      break;
    }

    case '4': {
      const outro = await prompt('Digite o nome da outra pessoa na conversa: ');
      const caminho = path.join(__dirname, '..', 'servidores', 'conversas_formatadas.json');

      if (fs.existsSync(caminho)) {
        const dados = JSON.parse(fs.readFileSync(caminho, 'utf-8'));
        const chave = [usuarioLogado, outro].sort().join('|');
        const conversa = dados[chave] || [];

        console.log(`\n💬 Conversa entre ${usuarioLogado} e ${outro}:`);
        for (const msg of conversa) {
          const lado = msg.from === usuarioLogado ? 'Você' : outro;
          console.log(`${lado}: ${msg.conteudo}`);
        }
      } else {
        console.log('⚠️ Nenhuma conversa registrada ainda.');
      }

      menu();
      break;
    }

    case '5':
      console.log('👋 Saindo...');
      rl.close();
      process.exit(0);
      break;

    default:
      console.log('Opção inválida!');
      menu();
  }
}

async function iniciar() {
  console.clear();
  usuarioLogado = await prompt('Digite seu nome de usuário para login: ');
  escutarPostagens(); // ← inicia stream de postagens após login
  menu();
}

iniciar();
