#!/bin/bash
# entrypoint.sh

echo "⏳ Ожидаю доступность PostgreSQL..."
while ! nc -z db 5432; do
  sleep 1
done

echo "✅ PostgreSQL доступен — запускаю бота"
python src/init_db.py && python -m src.main
