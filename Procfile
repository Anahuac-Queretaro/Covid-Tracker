web: gunicorn covid_tracker.wsgi:application --python app --log-file - --log-level debug --preload --workers 1
worker: celery worker --app=covid_tracker