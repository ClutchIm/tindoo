echo "storage_service: Ожидание PostgreSQL..."
while ! nc -z storage_db 5432; do sleep 1; done
echo "storage_service: PostgreSQL запущен."

echo "storage_service: Применяем миграции..."
python manage.py migrate --noinput

sleep 5

echo "storage_service: Запускаем сервер..."
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000