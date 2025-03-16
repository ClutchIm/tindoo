#!/bin/sh
echo "matching_service: Ожидание PostgreSQL..."
while ! nc -z matching_db 5432; do sleep 1; done
echo "matching_service: PostgreSQL запущен."

echo "matching_service: Ожидание Redis..."
while ! nc -z matching_redis 6379; do sleep 1; done
echo "matching_service: Redis запущен."

echo "matching_service: Применяем миграции..."
python manage.py migrate --noinput

sleep 5

echo "matching_service: Запускаем сервер..."
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000