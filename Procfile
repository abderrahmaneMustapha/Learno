web: gunicorn learno.wsgi
worker: celery -A learno worker -l info
release: python manage.py migrate
