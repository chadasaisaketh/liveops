\

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Incident(models.Model):
    STATUS_CHOICES = [
        ("OPEN", "Open"),
        ("RESOLVED", "Resolved"),
    ]

    TYPE_CHOICES = [
        ("DATABASE", "Database"),
        ("SERVER", "Server"),
        ("SECURITY", "Security"),
        ("NETWORK", "Network"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="OPEN"
    )

    

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.status})"

class Message(models.Model):
    incident = models.ForeignKey(
        Incident,
        related_name="messages",
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.content[:20]}"