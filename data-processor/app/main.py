from flask import Flask, render_template, request, jsonify
import psycopg2
import paho.mqtt.client as mqtt
import os

app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://admin:password@database:5432/industrial_db")
MQTT_BROKER = os.environ.get("MQTT_BROKER", "mqtt-broker")

# Обработчик сообщений MQTT
def on_message(client, userdata, message):
    payload = message.payload.decode('utf-8')
    topic = message.topic
    print(f"Получено сообщение: {payload} из топика: {topic}")

    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()

        if topic.endswith("/status"):
            device_id = topic.split("/")[1]
            cursor.execute(
                """
                INSERT INTO devices (device_id, status, last_updated) 
                VALUES (%s, %s, NOW()) 
                ON CONFLICT (device_id) 
                DO UPDATE SET status = EXCLUDED.status, last_updated = NOW();
                """,
                (device_id, payload)
            )

        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Ошибка записи в базу: {e}")

# MQTT-клиент
client = mqtt.Client()
client.on_message = on_message
client.connect(MQTT_BROKER, 1883, 60)
client.subscribe("industrial/#")
client.loop_start()

# Главная страница
@app.route('/')
def index():
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM devices;")
    device_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM messages;")
    message_count = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return render_template('index.html', device_count=device_count, message_count=message_count)

# Страница устройств
@app.route('/devices')
def devices():
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM devices;")
    devices = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('devices.html', devices=devices)

@app.route('/add-device', methods=['POST'])
def add_device():
    device_id = request.form.get('device_id')
    if not device_id:
        return jsonify({"error": "Device ID is required"}), 400
    
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO devices (device_id, status) VALUES (%s, %s) ON CONFLICT DO NOTHING;",
            (device_id, 'inactive')
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"status": "Device added", "device_id": device_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Страница сообщений
@app.route('/messages', methods=['GET'])
def messages():
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM messages;")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('messages.html', messages=rows)

# Отправка команды устройству
@app.route('/send-command', methods=['POST'])
def send_command():
    data = request.json
    device_id = data['device_id']
    command = data['command']
    client.publish(f"industrial/{device_id}/command", command)
    return jsonify({"status": "Command sent", "device_id": device_id, "command": command})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
