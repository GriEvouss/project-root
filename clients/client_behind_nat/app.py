from flask import Flask, request, jsonify
import socket

app = Flask(__name__)

@app.route('/connect', methods=['POST'])
def connect():
    """
    Имитирует установление соединения через NAT, отправляя данные
    серверу или другому клиенту.
    """
    target_ip = request.json.get('target_ip')
    target_port = request.json.get('target_port')

    if not target_ip or not target_port:
        return jsonify({"error": "Missing target IP or port"}), 400

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((target_ip, int(target_port)))
            s.sendall(b"Hello from NAT client!")
        return jsonify({"success": True, "message": "Connection established"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
