from django.db import models
from django.conf import settings

class Incident(models.Model):
    STATUS_CHOICES = (
        ("OPEN", "OPEN"),
        ("RESOLVED", "RESOLVED"),
    )

    TYPE_CHOICES = (
        ("DATABASE", "DATABASE"),
        ("SERVER", "SERVER"),
        ("NETWORK", "NETWORK"),
        ("OTHER", "OTHER"),
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="OPEN")
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ChatMessage(models.Model):
    incident = models.ForeignKey(
        Incident,
        on_delete=models.CASCADE,
        related_name="messages"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,   # ✅ FIX HERE
        on_delete=models.CASCADE
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:20]
