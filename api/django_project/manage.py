#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from ast import literal_eval

from opentelemetry.instrumentation.django import DjangoInstrumentor
from opentelemetry.instrumentation.elasticsearch import ElasticsearchInstrumentor
from opentelemetry.instrumentation.redis import RedisInstrumentor

DEBUG = literal_eval(os.environ.get("DEBUG_MODE", "True"))


def initialize_debugger():
    if DEBUG:
        try:
            import debugpy

            debugpy.listen(("0.0.0.0", 8069))
        except Exception:
            pass


def initialize_opentelemetry():
    DjangoInstrumentor().instrument(is_sql_commentor_enabled=True)
    ElasticsearchInstrumentor().instrument()
    RedisInstrumentor().instrument()


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    initialize_debugger()
    initialize_opentelemetry()
    main()
