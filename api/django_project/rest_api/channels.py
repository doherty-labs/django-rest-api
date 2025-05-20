from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer


class TaskProgressConsumer(JsonWebsocketConsumer):
    def celery_task_update(self, event: dict) -> None:
        message = event["message"]
        self.send_json(message)

    def connect(self) -> None:
        super().connect()
        task_id = self.scope.get("url_route").get("kwargs").get("taskID")
        async_to_sync(self.channel_layer.group_add)(task_id, self.channel_name)

    def receive(self, *_: tuple) -> None:
        self.send(text_data="Hello world!")

    def disconnect(self) -> None:
        self.close()
