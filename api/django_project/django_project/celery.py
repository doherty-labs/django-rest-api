import os

if os.environ.get("ENABLE_GEVENT_PATCH", "False").lower().strip() == "true":
    from gevent import monkey

    monkey.patch_all()

    from grpc.experimental.gevent import init_gevent

    init_gevent()


from datetime import timedelta
from pathlib import Path

import django
from celery import Celery, bootsteps
from celery.signals import beat_init, worker_process_init, worker_ready, worker_shutdown
from opentelemetry.instrumentation.celery import CeleryInstrumentor

# File for validating worker readiness
READINESS_FILE = Path("/tmp/celery_ready")  # noqa: S108
HEARTBEAT_FILE = Path("/tmp/celery_worker_heartbeat")  # noqa: S108

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project.settings")
django.setup()


class LivenessProbe(bootsteps.StartStopStep):
    requires = {"celery.worker.components:Timer"}  # noqa: RUF012

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.requests = []
        self.tref = None

    def start(self, worker):
        self.tref = worker.timer.call_repeatedly(
            1.0,
            self.update_heartbeat_file,
            (worker,),
            priority=10,
        )

    def stop(self, worker):
        HEARTBEAT_FILE.unlink(missing_ok=True)

    def update_heartbeat_file(self, worker):
        HEARTBEAT_FILE.touch()


@worker_ready.connect
def worker_ready_task(**_):
    READINESS_FILE.touch()


@worker_shutdown.connect
def worker_shutdown_task(**_):
    READINESS_FILE.unlink(missing_ok=True)


@beat_init.connect
def beat_ready(**_):
    READINESS_FILE.touch()


app = Celery("rest_api", include=["rest_api"])
app.steps["worker"].add(LivenessProbe)
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.result_chord_join_timeout = 900
app.conf.result_chord_retry_interval = 5
app.conf.result_expires = timedelta(days=3)
app.conf.broker_connection_retry_on_startup = True


@worker_process_init.connect(weak=False)
def init_celery_tracing(**_):
    CeleryInstrumentor().instrument()
