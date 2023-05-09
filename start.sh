python3 -m manage collectstatic
python3 -m manage migrate
gunicorn --bind 0.0.0.0:8000 smart_relays.wsgi --workers=4
