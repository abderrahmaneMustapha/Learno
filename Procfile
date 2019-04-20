web: gunicorn learno.wsgi
worker: celery -A learno worker
beat: celery -A learno beat -S django
