import logging
import sys
from pathlib import Path

logger = logging.getLogger(__name__)

PID_FILE = Path("/tmp/celery-beat.pid") # noqa: S108
if not PID_FILE.is_file():
    logger.error("Celery beat PID file NOT found.")
    sys.exit(1)

logger.info("Celery beat PID file found.")
sys.exit(0)
