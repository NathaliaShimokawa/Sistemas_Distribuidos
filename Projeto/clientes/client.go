package clientes

import (
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
	"log"
)

func CriarClienteGrpc(endereco string) (RedeSocialClient, *grpc.ClientConn) {
	conn, err := grpc.Dial(endereco, grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		log.Fatalf("Falha ao conectar: %v", err)
	}
	client := NewRedeSocialClient(conn)
	return client, conn
}

