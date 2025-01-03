from enum import StrEnum

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from pydantic import BaseModel


class WebsocketEventTypes(StrEnum):
    UPDATE_AVAILABILITY = "update_availability"


class WebsocketService:
    def __init__(
        self,
    ) -> None:
        self.channel_layer = get_channel_layer()

    def send_message(
        self,
        merchant_id: int,
        type_event: WebsocketEventTypes,
        message: BaseModel,
    ) -> None:
        async_to_sync(self.channel_layer.group_send)(
            "merchant_" + str(merchant_id),
            {
                "type": type_event.value,
                "message": message.json(),
            },
        )
