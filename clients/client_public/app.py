from flask import Flask, request, jsonify
import socket

app = Flask(__name__)

@app.route('/listen', methods=['GET'])
def listen():
    """
    Запускает серверный сокет для получения соединений от клиентов.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('0.0.0.0', 6000))
            s.listen(1)
            conn, addr = s.accept()
            with conn:
                print('Connected by', addr)
                data = conn.recv(1024)
                return jsonify({"success": True, "data": data.decode('utf-8')})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
