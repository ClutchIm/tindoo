echo "chat_service: Ожидание Redis..."
while ! nc -z chat_redis 6379; do sleep 1; done
echo "chat_service: Redis запущен."

echo "chat_service: Применяем миграции..."
python manage.py migrate --noinput

sleep 5

echo "chat_service: Запускаем сервер..."
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000