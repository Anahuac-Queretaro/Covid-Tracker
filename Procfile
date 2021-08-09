web: gunicorn covid_tracker.wsgi:application --python app --log-file - --log-level debug --preload --workers 1
worker: cd app && celery -A covid_tracker worker -l INFO