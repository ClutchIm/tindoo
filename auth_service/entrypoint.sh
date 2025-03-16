echo "auth_service: Ожидание PostgreSQL..."
while ! nc -z auth_db 5432; do sleep 1; done
echo "auth_service: PostgreSQL запущен."

echo "auth_service: Применяем миграции..."
python manage.py migrate --noinput

sleep 5

echo "auth_service: Запускаем сервер..."
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000