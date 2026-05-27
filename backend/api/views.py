from rest_framework import generics
from .models import SensorReading
from .serializers import SensorReadingSerializer

from ml.detector import predict_anomaly


class SensorReadingCreateView(generics.CreateAPIView):

    queryset = SensorReading.objects.all()
    serializer_class = SensorReadingSerializer

    def perform_create(self, serializer):

        reading = serializer.save()

        sensor_values = [
            reading.ion_gauge_pressure,
            reading.flowcool_pressure,
            reading.flowcool_flowrate
        ]

        score, is_anomaly = predict_anomaly(sensor_values)

        reading.anomaly_score = score
        reading.is_anomaly = is_anomaly

        reading.save()