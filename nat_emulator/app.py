from flask import Flask, request, jsonify
import socket
import threading

app = Flask(__name__)

# Таблица сопоставления для имитации NAT
nat_table = {}

@app.route('/register', methods=['POST'])
def register():
    """
    Регистрация клиента в NAT-таблице.
    Клиент за NAT регистрирует свой внутренний IP и порт.
    """
    client_id = request.json.get('client_id')
    internal_ip = request.json.get('internal_ip')
    internal_port = request.json.get('internal_port')

    if not client_id or not internal_ip or not internal_port:
        return jsonify({"error": "Missing client_id, internal_ip, or internal_port"}), 400

    nat_table[client_id] = {
        "internal_ip": internal_ip,
        "internal_port": internal_port
    }

    return jsonify({"success": True, "message": "Client registered", "client_id": client_id})

@app.route('/connect', methods=['POST'])
def connect():
    """
    Имитация проброса порта NAT для соединения клиентов.
    Публичный клиент подключается к клиенту за NAT через NAT-эмулятор.
    """
    source_id = request.json.get('source_id')
    target_id = request.json.get('target_id')

    if not source_id or not target_id:
        return jsonify({"error": "Missing source_id or target_id"}), 400

    if target_id not in nat_table:
        return jsonify({"error": "Target client not registered"}), 404

    target_info = nat_table[target_id]
    internal_ip = target_info["internal_ip"]
    internal_port = target_info["internal_port"]

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((internal_ip, int(internal_port)))
            s.sendall(b"Message from NAT Emulator")
        return jsonify({"success": True, "message": f"Connected to {target_id}"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/nat_table', methods=['GET'])
def get_nat_table():
    """
    Возвращает текущую NAT-таблицу.
    """
    return jsonify({"nat_table": nat_table})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
