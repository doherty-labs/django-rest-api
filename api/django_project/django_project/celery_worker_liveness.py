import logging
import sys
import time
from pathlib import Path

logger = logging.getLogger(__name__)

LIVENESS_FILE = Path("/tmp/celery_worker_heartbeat") # noqa: S108
if not LIVENESS_FILE.is_file():
    logger.error("Celery liveness file NOT found.")
    sys.exit(1)

stats = LIVENESS_FILE.stat()
heartbeat_timestamp = stats.st_mtime
current_timestamp = time.time()
time_diff = current_timestamp - heartbeat_timestamp
DELTA_THRESHOLD = 60

if time_diff > DELTA_THRESHOLD:
    logger.error(
        "Celery Worker liveness file timestamp DOES NOT matches the given constraint.",
    )
    sys.exit(1)

logger.info(
    "Celery Worker liveness file found and timestamp matches the given constraint.",
)
sys.exit(0)
