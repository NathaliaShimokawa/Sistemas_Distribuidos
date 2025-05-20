from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import random

app = Flask(__name__)

# Desvio de até ±1 segundo
MAX_DESVIO = 1.0

# Função utilitária para hora com desvio aleatório
def hora_atual_com_desvio():
    agora = datetime.utcnow()
    desvio = random.uniform(-MAX_DESVIO, MAX_DESVIO)
    hora_desviada = agora + timedelta(seconds=desvio)
    return hora_desviada

@app.route("/hora", methods=["GET"])
def obter_hora():
    hora = hora_atual_com_desvio()
    return jsonify({"hora": hora.isoformat()})

@app.route("/sincronizar", methods=["POST"])
def sincronizar():
    dados = request.get_json()
    hora_cliente_str = dados.get("hora_cliente")
    try:
        hora_cliente = datetime.fromisoformat(hora_cliente_str)
        hora_servidor = hora_atual_com_desvio()
        diferenca = (hora_servidor - hora_cliente).total_seconds()
        return jsonify({"ajuste_segundos": diferenca})
    except Exception as e:
        return jsonify({"erro": str(e)}), 400

if __name__ == "__main__":
    import sys
    porta = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    app.run(host="0.0.0.0", port=porta)
