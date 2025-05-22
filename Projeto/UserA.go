package main

import (
	"context"
	"fmt"
	"log"
	pb "projeto/clientes"
	"time"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
)

func main() {
	servers := []string{
		"localhost:50051",
		"localhost:50052",
		"localhost:50053",
	}

	userId := "UserA"
	relogioLogico := float64(time.Now().UnixMilli())
	relogioFisico := float64(time.Now().UnixNano()) / 1e9

	for _, addr := range servers {
		conn, err := grpc.Dial(addr, grpc.WithTransportCredentials(insecure.NewCredentials()))
		if err != nil {
			log.Printf("Falha ao conectar ao servidor %s: %v", addr, err)
			continue
		}
		defer conn.Close()

		client := pb.NewRedeSocialClient(conn)

		post := &pb.Postagem{
			UserId:          userId,
			Conteudo:        "Postagem do UserA.",
			TimestampLogico: relogioLogico,
			TimestampFisico: relogioFisico,
		}

		_, err = client.Postar(context.Background(), post)
		if err != nil {
			log.Printf("Erro ao postar no servidor %s: %v", addr, err)
		} else {
			fmt.Printf("UserA postou uma mensagem no servidor %s.\n", addr)
		}

		msg := &pb.Mensagem{
			From_:           userId,
			To:              "UserB",
			Conteudo:        "Oi UserB!",
			TimestampLogico: relogioLogico + 1,
		}

		_, err = client.EnviarMensagem(context.Background(), msg)
		if err != nil {
			log.Printf("Erro ao enviar mensagem no servidor %s: %v", addr, err)
		} else {
			fmt.Printf("UserA enviou uma mensagem para UserB no servidor %s.\n", addr)
		}
	}
}
