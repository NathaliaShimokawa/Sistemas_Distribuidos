const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');
const path = require('path');
const readline = require('readline');

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

let currentUser = null;

function promptMenu() {
  console.log('\n=== MENU ===');
  console.log('1 - Postar');
  console.log('2 - Enviar mensagem');
  console.log('3 - Seguir usuário');
  console.log('4 - Trocar usuário');
  console.log('0 - Sair');
  rl.question('Escolha uma opção: ', handleMenuOption);
}

function handleMenuOption(option) {
  switch (option) {
    case '1':
      rl.question('Conteúdo da postagem: ', conteudo => {
        const relogioLogico = Math.floor(Math.random() * 100);
        const relogioFisico = Date.now();

        const conteudoJsonString = JSON.stringify({
          user_id: currentUser,
          conteudo: conteudo
        });

        client.Postar({
          user_id: currentUser,
          conteudo: conteudoJsonString,
          timestamp_logico: relogioLogico,
          timestamp_fisico: relogioFisico
        }, (err, response) => {
          if (err) {
            console.error('Erro ao postar:', err.message);
          } else {
            console.log('Postagem feita com sucesso.');
          }
          promptMenu();
        });
      });
      break;

    case '2':
      rl.question('Destinatário: ', to => {
        rl.question('Mensagem: ', conteudo => {
          const relogioLogico = Math.floor(Math.random() * 100);

          client.EnviarMensagem({
            from_: currentUser,
            to: to,
            conteudo: conteudo,
            timestamp_logico: relogioLogico
          }, (err, res) => {
            if (err) {
              console.error('Erro ao enviar mensagem:', err.message);
            } else {
              console.log('Mensagem enviada com sucesso.');
            }
            promptMenu();
          });
        });
      });
      break;

    case '3':
      rl.question('ID do usuário a seguir: ', seguidoid => {
        client.Seguir({
          seguidorid: currentUser,
          seguidoid: seguidoid
        }, (err, res) => {
          if (err) {
            console.error('Erro ao seguir usuário:', err.message);
          } else {
            console.log(`Agora você segue ${seguidoid}.`);
          }
          promptMenu();
        });
      });
      break;

    case '4':
      escolherUsuario();
      break;

    case '0':
      console.log('Saindo...');
      rl.close();
      break;

    default:
      console.log('Opção inválida.');
      promptMenu();
  }
}

function escolherUsuario() {
  rl.question('Digite o ID do usuário atual: ', userId => {
    currentUser = userId.trim();
    console.log(`Usuário definido como: ${currentUser}`);
    promptMenu();
  });
}

console.log('Bem-vindo à Rede Social Distribuída!');
escolherUsuario();
