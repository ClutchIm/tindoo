#!/bin/sh
echo "user_profile_service: Ожидание PostgreSQL..."
while ! nc -z user_profile_db 5432; do sleep 1; done
echo "user_profile_service: PostgreSQL запущен."

echo "user_profile_service: Ожидание Redis..."
while ! nc -z user_profile_redis 6379; do sleep 1; done
echo "user_profile_service: Redis запущен."

echo "user_profile_service: Применяем миграции..."
python manage.py migrate --noinput

sleep 5

echo "user_profile_service: Запускаем сервер..."
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000