from rest_framework import serializers
from .models import SensorReading
from .models import Equipment


class SensorReadingSerializer(serializers.ModelSerializer):

    tool_id = serializers.CharField(
        write_only=True
    )

    class Meta:
        model = SensorReading

        fields = [
            "tool_id",
            "timestamp",
            "ion_gauge_pressure",
            "flowcool_pressure",
            "flowcool_flowrate"
        ]

    def create(self, validated_data):

        tool_id = validated_data.pop(
            "tool_id"
        )

        equipment = Equipment.objects.get(
            tool_id=tool_id
        )

        return SensorReading.objects.create(
            equipment=equipment,
            **validated_data
        )