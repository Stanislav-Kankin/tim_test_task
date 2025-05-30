#!/bin/bash
echo "⏳ Жду PostgreSQL..."
while ! nc -z db 5432; do
  sleep 0.5
done

echo "✅ PostgreSQL доступен — запускаю Django"
exec "$@"
