\

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


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

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="incidents"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.status})"
