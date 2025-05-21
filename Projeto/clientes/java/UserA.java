import io.grpc.ManagedChannel;
import io.grpc.ManagedChannelBuilder;
import redesocial.RedeSocialGrpc;
import redesocial.RedeSocialOuterClass.*;

import java.util.Random;

public class UserA {
    public static void main(String[] args) throws InterruptedException {
        ManagedChannel channel = ManagedChannelBuilder.forAddress("localhost", 50051)
                .usePlaintext()
                .build();

        RedeSocialGrpc.RedeSocialBlockingStub stub = RedeSocialGrpc.newBlockingStub(channel);

        String userId = "UserA";

        // Simular relógio lógico e físico
        int relogioLogico = new Random().nextInt(100);
        double relogioFisico = System.currentTimeMillis() / 1000.0;

        // Postar algo
        PostRequest postRequest = PostRequest.newBuilder()
                .setUserId(userId)
                .setConteudo("Olá! Essa é a postagem de UserA")
                .setTimestampLogico(relogioLogico)
                .setTimestampFisico(relogioFisico)
                .build();

        stub.postar(postRequest);
        System.out.println("UserA postou.");

        // Seguir UserB
        FollowRequest followRequest = FollowRequest.newBuilder()
                .setSeguidorId(userId)
                .setSeguidoId("UserB")
                .build();

        stub.seguir(followRequest);
        System.out.println("UserA agora segue UserB.");

        channel.shutdown();
    }
}
