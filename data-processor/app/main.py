import os
import psycopg2
import paho.mqtt.client as mqtt
from flask import Flask, jsonify

app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://admin:password@database:5432/industrial_db")
MQTT_BROKER = os.environ.get("MQTT_BROKER", "mqtt-broker")

# Обработчик сообщений
def on_message(client, userdata, message):
    payload = message.payload.decode('utf-8')
    print(f"Получено сообщение: {payload}")
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO messages (content) VALUES (%s)", (payload,))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Ошибка записи в базу: {e}")

# Настройка MQTT
client = mqtt.Client()
client.on_message = on_message
client.connect(MQTT_BROKER, 1883, 60)
client.subscribe("industrial/devices")
client.loop_start()

@app.route('/messages', methods=['GET'])
def get_messages():
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM messages;")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(rows)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
