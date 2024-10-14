#!/usr/bin/env bash
set -e
cd ./django
rm -rf ./staticfiles
python manage.py collectstatic --noinput
if [ "$DJANGO_HOT_RELOAD" = "true" ]
then
    python manage.py migrate
    exec python manage.py runserver 0.0.0.0:8000
else
    exec gunicorn django_project.asgi:application -k uvicorn_worker.UvicornWorker --bind 0.0.0.0:8000 --workers $GUNICORN_WORKERS
fi

