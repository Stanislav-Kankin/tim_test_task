#!/bin/bash

echo "⏳ Жду PostgreSQL..."
while ! nc -z db 5432; do
  sleep 1
done

echo "✅ PostgreSQL доступен — запускаю Django"

python manage.py migrate --noinput

echo "Создаю суперпользователя..."
echo "from django.contrib.auth import get_user_model; \
User = get_user_model(); \
User.objects.filter(username='admin').exists() or \
User.objects.create_superuser('admin', 'admin@example.com', 'admin123')" \
| python manage.py shell

python manage.py runserver 0.0.0.0:8000
