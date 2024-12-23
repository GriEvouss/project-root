import paho.mqtt.client as mqtt
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
