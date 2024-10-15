#!/usr/bin/env bash
set -e
cd ./django
rm -rf ./staticfiles
if [ "$DEBUG_MODE" = "True" ]
then
    python manage.py collectstatic --noinput
    python manage.py migrate
    exec python manage.py runserver 0.0.0.0:8000
else
    exec gunicorn django_project.asgi:application -k uvicorn_worker.UvicornWorker --bind 0.0.0.0:8000 --workers $GUNICORN_WORKERS
fi

