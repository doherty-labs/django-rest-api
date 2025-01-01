import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class HcpVaultSecrets:
    def __init__(
        self,
    ) -> None:
        self.secret_file_path = "/etc/secret-volume"  # noqa: S105

    def get_secret(self, name: str, default_value: str) -> str:
        logger.info("Reading secret from file")
        try:
            path = Path(Path(self.secret_file_path) / name)
            with path.open() as f:
                return f.read().strip()
        except FileNotFoundError:
            msg = f"Secret file {name} not found"
            logger.exception(msg)
            return default_value
