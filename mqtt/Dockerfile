# Используем официальный образ Mosquitto
FROM eclipse-mosquitto:latest

# Копируем конфигурацию
COPY mosquitto.conf /mosquitto/config/mosquitto.conf

# Открываем порты для MQTT
EXPOSE 1883 9001

# Команда запуска
CMD ["mosquitto", "-c", "/mosquitto/config/mosquitto.conf"]
