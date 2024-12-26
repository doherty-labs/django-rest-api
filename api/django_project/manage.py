#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os  # noqa: E402

if os.environ.get("ENABLE_GEVENT_PATCH", "False").lower().strip() == "true":
    from gevent import monkey  # noqa: E402

    monkey.patch_all()  # noqa: E402

    from grpc.experimental.gevent import init_gevent  # noqa: E402

    init_gevent()  # noqa: E402

import os  # noqa: E402, F404
import sys  # noqa: E402, F404
from ast import literal_eval  # noqa: E402, F404

DEBUG = literal_eval(os.environ.get("DEBUG_MODE", "True"))


def initialize_debugger():
    if DEBUG:
        try:
            import debugpy

            debugpy.listen(("0.0.0.0", 8069))
        except Exception:
            pass


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
    main()
