web: gunicorn config.wsgi:application
worker: celery worker --app=network_search.taskapp --loglevel=info
