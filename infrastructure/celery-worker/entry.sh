#!/usr/bin/env bash
set -e
cd ./django
exec celery -A django_project worker -P gevent -c 1000 --loglevel=debug --scheduler django_celery_beat.schedulers:DatabaseScheduler 
