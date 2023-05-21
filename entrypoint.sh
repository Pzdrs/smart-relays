python3 -m manage collectstatic --no-input
python3 -m manage migrate --no-input

celery -A smart_relays worker -l info &

gunicorn --bind 0.0.0.0:8000 smart_relays.wsgi
