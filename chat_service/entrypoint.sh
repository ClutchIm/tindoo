#!/bin/sh
echo "Ожидание Redis..."
while ! nc -z chat_redis 6379; do sleep 1; done
echo "Redis запущен."

echo "Применяем миграции..."
python manage.py migrate --noinput

sleep 5

echo "Запускаем сервер..."
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000