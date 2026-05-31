from rest_framework import generics
from .models import SensorReading
from .serializers import SensorReadingSerializer

from ml.detector import predict_anomaly
from ml.detector import calculate_health_score
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Equipment

from ml.ttf_predictor import predict_ttf

MACHINE_MAP = {
    "01_M01": 0,
    "01_M02": 1,
    "02_M01": 2,
    "03_M02": 3,
    "04_M01": 4,
    "04_M02": 5,
    "05_M01": 6,
    "05_M02": 7,
    "06_M01": 8,
    "06_M02": 9,
    "07_M01": 10,
    "08_M01": 11,
    "09_M01": 12,
    "10_M01": 13
}

class SensorReadingCreateView(generics.CreateAPIView):

    queryset = SensorReading.objects.all()
    serializer_class = SensorReadingSerializer

    def perform_create(self, serializer):

        

        reading = serializer.save()

        anomaly_features = [
            reading.ion_gauge_pressure,
            reading.flowcool_pressure,
            reading.flowcool_flowrate
        ]

        score, is_anomaly = predict_anomaly(
            anomaly_features
        )

        health = calculate_health_score(
            score
        )

        machine_id = MACHINE_MAP.get(
            reading.equipment.tool_id,
            0
        )

        ttf_features = [
            reading.etch_source_usage,
            reading.etch_aux_source_timer,
            reading.etch_aux2_source_timer,
            reading.etch_beam_current,
            reading.flowcool_pressure,
            reading.rotation_speed,
            reading.actual_step_duration,
            reading.ion_gauge_pressure,
            reading.etch_beam_voltage,
            reading.actual_rotation_angle,
            machine_id
        ]

        predicted_ttf = predict_ttf(
            ttf_features
        )
        

        reading.health_score = health
        reading.anomaly_score = score
        reading.is_anomaly = is_anomaly
        reading.predicted_ttf = predicted_ttf

        

        reading.save()

        

class EquipmentHealthView(APIView):

    def get(self, request, equipment_id):

        equipment = Equipment.objects.get(id=equipment_id)

        latest_reading = (
        equipment.readings
        .exclude(health_score__isnull=True)
        .order_by("-id")
        .first()
        )

        if latest_reading is None:
            return Response({
                "message": "No readings found"
            })

        return Response({
            "tool_id": equipment.tool_id,
            "health_score": latest_reading.health_score,
            "is_anomaly": latest_reading.is_anomaly,
            "timestamp": latest_reading.timestamp,
            "predicted_ttf": latest_reading.predicted_ttf
        })
    
class RecentReadingsView(APIView):

    def get(self, request, equipment_id):

        equipment = Equipment.objects.get(id=equipment_id)

        readings = (
            equipment.readings
            .order_by("-timestamp")[:100]
        )

        data = []

        for reading in readings:

            data.append({
                "timestamp": reading.timestamp,
                "flowcool_pressure": reading.flowcool_pressure,
                "health_score": reading.health_score,
                "anomaly_score": reading.anomaly_score
            })

        return Response(data)
    


class AlertsView(APIView):

    def get(self, request):

        alerts = []

        readings = (
            Equipment.objects
            .first()
            .readings
            .order_by("-timestamp")[:100]
        )

        for reading in readings:

            if reading.health_score is not None and reading.health_score < 60:

                alerts.append({
                    "timestamp": reading.timestamp,
                    "message": "Equipment health below threshold",
                    "health_score": reading.health_score
                })

        return Response(alerts)
    

class EquipmentListView(APIView):

    def get(self, request):

        equipment = Equipment.objects.all()

        data = []

        for eq in equipment:
            data.append({
                "id": eq.id,
                "tool_id": eq.tool_id
            })

        return Response(data)
    
class FleetHealthView(APIView):

    def get(self, request):

        data = []

        for equipment in Equipment.objects.all():

            latest_reading = (
                equipment.readings
                .exclude(health_score__isnull=True)
                .order_by("-id")
                .first()
            )

            if latest_reading:

                data.append({
                    "tool_id": equipment.tool_id,
                    "health_score": latest_reading.health_score,
                    "is_anomaly": latest_reading.is_anomaly
                })

        return Response(data)
    
