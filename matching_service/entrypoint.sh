#!/bin/sh
echo "Ожидание PostgreSQL..."
while ! nc -z matching_db 5432; do sleep 1; done
echo "PostgreSQL запущен."

echo "Ожидание Redis..."
while ! nc -z matching_redis 6379; do sleep 1; done
echo "Redis запущен."

echo "Применяем миграции..."
python manage.py migrate --noinput

sleep 2

echo "Запускаем сервер..."
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000