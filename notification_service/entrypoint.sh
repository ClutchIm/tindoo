echo "notification_service: Ожидание Redis..."
while ! nc -z notification_redis 6379; do sleep 1; done
echo "notification_service: Redis запущен."

echo "notification_service: Применяем миграции..."
python manage.py migrate --noinput

sleep 5

echo "notification_service: Запускаем сервер..."
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000