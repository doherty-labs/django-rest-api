import sys
from pathlib import Path

READINESS_FILE = Path("/tmp/celery_ready")  # noqa: S108
if not READINESS_FILE.is_file():
    sys.exit(1)
sys.exit(0)
