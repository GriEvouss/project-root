import paho.mqtt.client as mqtt
from flask import Flask, jsonify
import psycopg2

# Настройки MQTT
MQTT_BROKER = "mqtt-broker"
MQTT_PORT = 1883
MQTT_TOPIC = "industrial/devices"

# Настройки базы данных
DATABASE_URL = "postgresql://admin:password@database:5432/industrial_db"

# Callback при получении сообщения
def on_message(client, userdata, message):
    payload = message.payload.decode()
    print(f"Получено сообщение: {payload}")

    # Сохранение в базу данных
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO messages (content) VALUES (%s)", (payload,))
    conn.commit()
    cursor.close()
    conn.close()

# Настройка MQTT-клиента
client = mqtt.Client()
client.on_message = on_message
client.connect(MQTT_BROKER, MQTT_PORT)
client.subscribe(MQTT_TOPIC)

# Бесконечный цикл
client.loop_forever()

app = Flask(__name__)

def get_messages():
    conn = psycopg2.connect("dbname=industrial_db user=admin password=password host=database")
    cur = conn.cursor()
    cur.execute("SELECT * FROM messages;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

@app.route('/messages', methods=['GET'])
def messages():
    data = get_messages()
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)