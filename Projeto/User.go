package main

import (
	"bufio"
	"context"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"path/filepath"
	"strings"
	"time"

	pb "projeto/clientes"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
)

var client pb.RedeSocialClient
var usuarioLogado string
var caminhoConversas string = filepath.Join("..", "servidores", "conversas_formatadas.json")

func conectarServidor() {
	conn, err := grpc.Dial("localhost:50051", grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		log.Fatalf("Erro ao conectar: %v", err)
	}
	client = pb.NewRedeSocialClient(conn)
}

func prompt(mensagem string) string {
	fmt.Print(mensagem)
	reader := bufio.NewReader(os.Stdin)
	texto, _ := reader.ReadString('\n')
	return strings.TrimSpace(texto)
}

func postar() {
	conteudo := prompt("Digite o conteúdo da postagem: ")
	relogioLogico := float64(time.Now().UnixMilli())
	relogioFisico := float64(time.Now().UnixNano()) / 1e9

	dados := map[string]string{
		"user_id":  usuarioLogado,
		"conteudo": conteudo,
	}
	conteudoJSON, _ := json.Marshal(dados)

	_, err := client.Postar(context.Background(), &pb.Postagem{
		UserId:          usuarioLogado,
		Conteudo:        string(conteudoJSON),
		TimestampLogico: relogioLogico,
		TimestampFisico: relogioFisico,
	})

	if err != nil {
		fmt.Println("Erro ao postar:", err)
	} else {
		fmt.Println("Postagem enviada com sucesso.")
	}
}

func enviarMensagem() {
	destino := prompt("Para quem deseja enviar mensagem? ")
	conteudo := prompt("Digite a mensagem: ")
	relogioLogico := float64(time.Now().UnixMilli())

	_, err := client.EnviarMensagem(context.Background(), &pb.Mensagem{
		From_:           usuarioLogado,
		To:              destino,
		Conteudo:        conteudo,
		TimestampLogico: relogioLogico,
	})

	if err != nil {
		fmt.Println("Erro ao enviar mensagem:", err)
	} else {
		fmt.Printf("Mensagem enviada para %s.\n", destino)
	}
}

func seguir() {
	seguido := prompt("Quem você quer seguir? ")

	_, err := client.Seguir(context.Background(), &pb.SeguirRequest{
		SeguidoId:  seguido,
		SeguidorId: usuarioLogado,
	})

	if err != nil {
		fmt.Println("Erro ao seguir:", err)
	} else {
		fmt.Printf("Agora você segue %s.\n", seguido)
	}
}

func verConversa() {
	outro := prompt("Digite o nome da outra pessoa na conversa: ")

	if _, err := os.Stat(caminhoConversas); os.IsNotExist(err) {
		fmt.Println("Nenhuma conversa registrada ainda.")
		return
	}

	dados, err := ioutil.ReadFile(caminhoConversas)
	if err != nil {
		fmt.Println("Erro ao ler conversas:", err)
		return
	}

	var conversas map[string][]map[string]interface{}
	json.Unmarshal(dados, &conversas)

	chave := []string{usuarioLogado, outro}
	if usuarioLogado > outro {
		chave[0], chave[1] = chave[1], chave[0]
	}
	chaveConcat := strings.Join(chave, "|")

	conversa := conversas[chaveConcat]

	fmt.Printf("\nConversa entre %s e %s:\n", usuarioLogado, outro)
	for _, msg := range conversa {
		lado := "Você"
		if msg["from"] != usuarioLogado {
			lado = outro
		}
		fmt.Printf("%s: %s\n", lado, msg["conteudo"])
	}
}

func menu() {
	for {
		fmt.Printf("\nBem-vindo, %s!\n", usuarioLogado)
		fmt.Println("1 - Postar")
		fmt.Println("2 - Enviar mensagem")
		fmt.Println("3 - Seguir alguém")
		fmt.Println("4 - Ver conversa com alguém")
		fmt.Println("5 - Sair")

		opcao := prompt("\nEscolha uma opção: ")

		switch opcao {
		case "1":
			postar()
		case "2":
			enviarMensagem()
		case "3":
			seguir()
		case "4":
			verConversa()
		case "5":
			fmt.Println("Saindo...")
			os.Exit(0)
		default:
			fmt.Println("Opção inválida!")
		}
	}
}

func main() {
	conectarServidor()
	fmt.Print("Digite seu nome de usuário para login: ")
	fmt.Scanln(&usuarioLogado)

	menu()
}
