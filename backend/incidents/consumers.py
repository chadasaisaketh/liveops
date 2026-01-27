import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope.get("user")

        if not user or user.is_anonymous:
            await self.close()
            return

        self.incident_id = self.scope["url_route"]["kwargs"]["incident_id"]
        self.room_group_name = f"chat_{self.incident_id}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, "room_group_name"):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get("message")

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "username": self.scope["user"].username,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "username": event["username"],
            "content": event["message"],
        }))
