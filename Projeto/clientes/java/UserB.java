import io.grpc.ManagedChannel;
import io.grpc.ManagedChannelBuilder;
import redesocial.RedeSocialGrpc;
import redesocial.RedeSocialOuterClass.*;

import java.util.Random;

public class UserB {
    public static void main(String[] args) throws InterruptedException {
        ManagedChannel channel = ManagedChannelBuilder.forAddress("localhost", 50052)
                .usePlaintext()
                .build();

        RedeSocialGrpc.RedeSocialBlockingStub stub = RedeSocialGrpc.newBlockingStub(channel);

        String userId = "UserB";

        // Simular relógio lógico e físico
        int relogioLogico = new Random().nextInt(100);
        double relogioFisico = System.currentTimeMillis() / 1000.0;

        // Postar algo
        PostRequest postRequest = PostRequest.newBuilder()
                .setUserId(userId)
                .setConteudo("Oi! Aqui é o UserB")
                .setTimestampLogico(relogioLogico)
                .setTimestampFisico(relogioFisico)
                .build();

        stub.postar(postRequest);
        System.out.println("UserB postou.");

        // Enviar mensagem para UserA
        MessageRequest msg = MessageRequest.newBuilder()
                .setFrom(userId)
                .setTo("UserA")
                .setConteudo("Olá UserA, tudo bem?")
                .setTimestampLogico(relogioLogico + 1)
                .build();

        stub.enviarMensagem(msg);
        System.out.println("UserB enviou mensagem para UserA.");

        channel.shutdown();
    }
}
