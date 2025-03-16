#!/bin/sh
echo "selection_deck_service: Ожидание PostgreSQL..."
while ! nc -z selection_deck_db 5432; do sleep 1; done
echo "selection_deck_service: PostgreSQL запущен."

echo "selection_deck_service: Применяем миграции..."
python manage.py migrate --noinput

sleep 5

echo "selection_deck_service: Запускаем сервер..."
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000