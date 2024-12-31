#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

import os

if os.environ.get("ENABLE_GEVENT_PATCH", "False").lower().strip() == "true":
    from gevent import monkey

    monkey.patch_all()

    from grpc.experimental.gevent import init_gevent

    init_gevent()

import os
import sys
from ast import literal_eval

DEBUG = literal_eval(os.environ.get("DEBUG_MODE", "True"))


def initialize_debugger() -> None:
    if DEBUG:
        try:
            import debugpy

            debugpy.listen(("0.0.0.0", 8069))
        except Exception:
            pass


def main() -> None:
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        msg = (
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        )
        raise ImportError(
            msg,
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    initialize_debugger()
    main()
