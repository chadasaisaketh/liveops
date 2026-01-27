from rest_framework import serializers
from .models import Incident

class IncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incident
        fields = [
            "id",
            "title",
            "description",
            "status",
            "type",
            "created_at",
        ]
        read_only_fields = ["id", "status", "created_at"]

    def validate_type(self, value):
        allowed = ["DATABASE", "SERVER", "NETWORK", "OTHER"]
        if value not in allowed:
            raise serializers.ValidationError(
                f"type must be one of {allowed}"
            )
        return value
