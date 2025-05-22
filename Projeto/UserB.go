package main

import (
	"context"
	"fmt"
	"log"
	"time"

	pb "projeto/clientes" // Importa o pacote gerado pelo protoc
)

func main() {
	// Criar cliente gRPC usando a função auxiliar do pacote
	client, conn := pb.CriarClienteGrpc("localhost:50051")
	defer conn.Close()

	// Dados do usuário
	userId := "UserB"
	relogioLogico := float64(time.Now().UnixMilli())        // Timestamp lógico
	relogioFisico := float64(time.Now().UnixNano()) / 1e9   // Timestamp físico

	// Fazer postagem
	post := &pb.Postagem{
		UserId:          userId,
		Conteudo:        "Postagem do UserB.",
		TimestampLogico: relogioLogico,
		TimestampFisico: relogioFisico,
	}

	_, err := client.Postar(context.Background(), post)
	if err != nil {
		log.Fatalf("Erro ao postar: %v", err)
	}
	fmt.Println("UserB postou uma mensagem.")

	// Enviar mensagem
	msg := &pb.Mensagem{
		From_:           userId,
		To:              "UserA",
		Conteudo:        "Oi UserA! Como vai?",
		TimestampLogico: relogioLogico + 1,
	}

	_, err = client.EnviarMensagem(context.Background(), msg)
	if err != nil {
		log.Fatalf("Erro ao enviar mensagem: %v", err)
	}
	fmt.Println("UserB enviou uma mensagem para UserA.")
}
