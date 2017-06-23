web: newrelic-admin run-program gunicorn config.wsgi:application
worker: celery worker --app=network_search.taskapp --loglevel=info
release: python manage.py migrate
