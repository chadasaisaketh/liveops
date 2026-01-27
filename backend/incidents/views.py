from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Incident
from .serializers import IncidentSerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_incidents(request):
    incidents = Incident.objects.all().order_by("-created_at")
    serializer = IncidentSerializer(incidents, many=True)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_incident(request):
    serializer = IncidentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def resolve_incident(request, id):
    try:
        incident = Incident.objects.get(id=id)
    except Incident.DoesNotExist:
        return Response({"error": "Incident not found"}, status=404)

    incident.status = "RESOLVED"
    incident.save()

    return Response({"message": "Incident resolved"})
