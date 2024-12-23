# Используем базовый образ Python
FROM python:3.9-slim

# Устанавливаем зависимости
RUN pip install paho-mqtt psycopg2-binary flask

# Копируем приложение
COPY app /app
WORKDIR /app

# Открываем порт для API
EXPOSE 5000

# Запускаем приложение
CMD ["python", "main.py"]
