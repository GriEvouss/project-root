import os
import psycopg2
import paho.mqtt.client as mqtt
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://admin:password@database:5432/industrial_db")
MQTT_BROKER = os.environ.get("MQTT_BROKER", "mqtt-broker")

# Обработчик сообщений
def on_message(client, userdata, message):
    payload = message.payload.decode('utf-8')
    topic = message.topic
    print(f"Получено сообщение: {payload} из топика: {topic}")

    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()

        # Если сообщение приходит с топика status, обновляем статус устройства
        if topic.endswith("/status"):
            device_id = topic.split("/")[1]
            cursor.execute(
                "INSERT INTO devices (device_id, status, last_updated) VALUES (%s, %s, NOW()) "
                "ON CONFLICT (device_id) DO UPDATE SET status = EXCLUDED.status, last_updated = NOW();",
                (device_id, payload)
            )
        # Если сообщение другого типа, можно добавлять логику обработки здесь

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

# Веб-интерфейс
@app.route('/')
def index():
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM devices;")
    devices = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('devices.html', devices=devices)

@app.route('/send-command', methods=['POST'])
def send_command():
    data = request.json
    device_id = data['device_id']
    command = data['command']
    client.publish(f"industrial/{device_id}/command", command)
    return jsonify({"status": "Command sent"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
