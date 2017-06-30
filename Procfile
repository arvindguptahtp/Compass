web: newrelic-admin run-program gunicorn config.wsgi:application
worker: REMAP_SIGTERM=SIGQUIT celery worker --app=network_search.taskapp --loglevel=info
release: python manage.py migrate
