# Используем официальный образ Python
FROM python:3.11-slim

# Установка системных зависимостей для SC2 Linux бинарников
RUN apt-get update && apt-get install -y --no-install-recommends \
    unzip \
    wget \
    libfontconfig1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libosmesa6 \
    libglu1-mesa \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Установка зависимостей бота
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код бота
COPY . .

# Переменная окружения для библиотеки python-sc2
# Указывает, где в контейнере будет лежать игра
ENV SC2PATH=/app/StarCraftII

# По умолчанию запускаем нашего модульного бота
# Флаг --headless (если мы его добавим в код) будет важен
CMD ["python", "bots/protoss_bot/main.py"]
