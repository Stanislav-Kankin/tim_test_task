#!/bin/bash

echo "⏳ Ожидаю доступность PostgreSQL..."
while ! nc -z db 5432; do
  sleep 1
done

echo "✅ PostgreSQL доступен — создаю таблицы..."

export PYTHONPATH=/app/src
python -m init_db

echo "🚀 Запускаю Telegram-бота..."
python -m main
