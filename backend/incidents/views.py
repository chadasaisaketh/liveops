from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Incident
from .serializers import IncidentSerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_incidents(request):
    incidents = Incident.objects.all().order_by("-created_at")
    serializer = IncidentSerializer(incidents, many=True)
    return Response(serializer.data)
