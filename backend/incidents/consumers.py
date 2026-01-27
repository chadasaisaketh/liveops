import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Incident, ChatMessage


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope.get("user")

        if not user or user.is_anonymous:
            await self.close()
            return

        self.user = user
        self.incident_id = int(self.scope["url_route"]["kwargs"]["incident_id"])
        self.room_group_name = f"chat_{self.incident_id}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # ✅ SEND CHAT HISTORY (late joiners)
        messages = await self.get_chat_history()
        await self.send(text_data=json.dumps({
            "type": "history",
            "messages": messages
        }))

    async def disconnect(self, close_code):
        if hasattr(self, "room_group_name"):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    # =========================
    # 🔥 THIS WAS MISSING
    # =========================
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get("message")

        if not message:
            return

        # ✅ Save to DB
        await self.save_message(message)

        # ✅ Broadcast to room
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "username": self.user.username,
                "content": message,
            }
        )

    # =========================
    # 🔥 THIS WAS MISSING
    # =========================
    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "username": event["username"],
            "content": event["content"],
        }))

    # =========================
    # DB OPERATIONS
    # =========================
    @database_sync_to_async
    def save_message(self, content):
        incident = Incident.objects.get(id=self.incident_id)
        ChatMessage.objects.create(
            incident=incident,
            user=self.user,
            content=content
        )

    @database_sync_to_async
    def get_chat_history(self):
        return [
            {
                "username": msg.user.username,
                "content": msg.content,
                "timestamp": msg.timestamp.isoformat()
            }
            for msg in ChatMessage.objects
            .filter(incident_id=self.incident_id)
            .order_by("timestamp")
        ]
