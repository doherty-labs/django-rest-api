from __future__ import annotations

import logging

from asgiref.sync import async_to_sync
from onepassword.client import Client

logger = logging.getLogger(__name__)


class OnePasswordService:
    def __init__(self, token: str) -> None:
        self.token = token
        if token == "":
            self.client = None
            return
        self.client = async_to_sync(self._get_client)()

    async def _get_client(self) -> Client:
        return await Client.authenticate(
            auth=self.token,
            integration_name="Django Project",
            integration_version="1.0.0",
        )

    async def _resolve(self, secret_reference: str) -> str:
        try:
            return await self.client.secrets.resolve(secret_reference)
        except Exception:
            msg = f"Failed to resolve secret reference {secret_reference}"
            logger.exception(msg)
            return None

    def get_item(self, item_id: str) -> str | None:
        if not self.client:
            logger.error("OnePassword client is not initialized.")
            return None

        return async_to_sync(self._resolve)(item_id)
