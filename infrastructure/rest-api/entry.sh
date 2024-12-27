#!/usr/bin/env bash
set -e
cd ./django
rm -rf ./staticfiles

if [ "$ASYNC_MODE" = "True" ]; then
    exec gunicorn django_project.asgi:application -k uvicorn_worker.UvicornWorker --bind 0.0.0.0:8000 --workers $GUNICORN_WORKERS --reload
fi

exec gunicorn django_project.wsgi:application --bind 0.0.0.0:8000 --workers $GUNICORN_WORKERS --worker-class gevent --reload