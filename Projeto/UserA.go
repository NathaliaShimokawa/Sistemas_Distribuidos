package main

import (
	"context"
	"fmt"
	"log"
	"time"

	pb "projeto/clientes" // Importa o pacote gerado a partir do proto
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
)

func main() {
	conn, err := grpc.Dial("localhost:50051", grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		log.Fatalf("Falha ao conectar: %v", err)
	}
	defer conn.Close()

	client := pb.NewRedeSocialClient(conn)

	userId := "UserA"
	relogioLogico := float64(time.Now().UnixMilli())
	relogioFisico := float64(time.Now().UnixNano()) / 1e9

	post := &pb.Postagem{
		UserId:          userId,
		Conteudo:        "Postagem do UserA.",
		TimestampLogico: relogioLogico,
		TimestampFisico: relogioFisico,
	}

	_, err = client.Postar(context.Background(), post)
	if err != nil {
		log.Fatalf("Erro ao postar: %v", err)
	}
	fmt.Println("UserA postou uma mensagem.")

	msg := &pb.Mensagem{
		From_:           userId,
		To:              "UserB",
		Conteudo:        "Oi UserB!",
		TimestampLogico: relogioLogico + 1,
	}

	_, err = client.EnviarMensagem(context.Background(), msg)
	if err != nil {
		log.Fatalf("Erro ao enviar mensagem: %v", err)
	}
	fmt.Println("UserA enviou uma mensagem para UserB.")
}
