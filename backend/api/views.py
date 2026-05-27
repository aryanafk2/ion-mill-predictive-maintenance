from rest_framework import generics
from .models import SensorReading
from .serializers import SensorReadingSerializer


class SensorReadingCreateView(generics.CreateAPIView):
    queryset = SensorReading.objects.all()
    serializer_class = SensorReadingSerializer