package main

import (
	"context"
	"fmt"
	"log"
	"time"

	pb "projeto/clientes" // Importa o pacote gerado pelo protoc
)

func main() {
	servers := []string{
		"localhost:50051",
		"localhost:50052",
		"localhost:50053",
	}

	userId := "UserB"
	relogioLogico := float64(time.Now().UnixMilli())      // Timestamp lógico
	relogioFisico := float64(time.Now().UnixNano()) / 1e9 // Timestamp físico

	for _, addr := range servers {
		client, conn := pb.CriarClienteGrpc(addr)
		if conn == nil {
			log.Printf("Não foi possível conectar ao servidor %s", addr)
			continue
		}
		defer conn.Close()

		// Fazer postagem
		post := &pb.Postagem{
			UserId:          userId,
			Conteudo:        "Postagem do UserB.",
			TimestampLogico: relogioLogico,
			TimestampFisico: relogioFisico,
		}

		_, err := client.Postar(context.Background(), post)
		if err != nil {
			log.Printf("Erro ao postar no servidor %s: %v", addr, err)
		} else {
			fmt.Printf("UserB postou uma mensagem no servidor %s.\n", addr)
		}

		// Enviar mensagem
		msg := &pb.Mensagem{
			From_:           userId,
			To:              "UserA",
			Conteudo:        "Oi UserA! Como vai?",
			TimestampLogico: relogioLogico + 1,
		}

		_, err = client.EnviarMensagem(context.Background(), msg)
		if err != nil {
			log.Printf("Erro ao enviar mensagem no servidor %s: %v", addr, err)
		} else {
			fmt.Printf("UserB enviou uma mensagem para UserA no servidor %s.\n", addr)
		}
	}
}
