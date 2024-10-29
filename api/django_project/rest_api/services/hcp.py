import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class HcpVaultSecrets:
    def __init__(
        self,
    ):
        self.secret_file_path = "/etc/secret-volume"

    def get_secret(self, name, default_value) -> str:
        logger.info("Reading secret from file")
        try:
            with open(Path(self.secret_file_path) / name, "r") as f:
                return f.read().strip()
        except FileNotFoundError:
            logger.error(f"Secret file {name} not found")
            return default_value
