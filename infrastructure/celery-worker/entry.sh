#!/usr/bin/env bash
set -e
cd ./django

QUEUE="${QUEUE:-celery,io_bound,cpu_bound}"
WORKER_POOL="${WORKER_POOL:-prefork}"
CONCURRENCY="${CONCURRENCY:-2}"
SCHEDULER="${SCHEDULER:-django_celery_beat.schedulers:DatabaseScheduler}"

exec celery -A django_project worker -P "$WORKER_POOL" -Q "$QUEUE" -c "$CONCURRENCY" --scheduler "$SCHEDULER" -E -l DEBUG