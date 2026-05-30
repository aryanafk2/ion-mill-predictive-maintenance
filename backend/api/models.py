from django.db import models


class Equipment(models.Model):
    tool_id = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.tool_id


class SensorReading(models.Model):

    equipment = models.ForeignKey(
        Equipment,
        on_delete=models.CASCADE,
        related_name='readings'
    )

    timestamp = models.FloatField()

    ion_gauge_pressure = models.FloatField()
    flowcool_pressure = models.FloatField()
    flowcool_flowrate = models.FloatField()

    anomaly_score = models.FloatField(
        null=True,
        blank=True
    )

    is_anomaly = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(auto_now_add=True)

    health_score = models.FloatField(
        null=True,
        blank=True
    )
    
    predicted_ttf = models.FloatField(
        null=True,
        blank=True
    )
    def __str__(self):
        return f"{self.equipment.tool_id} - {self.timestamp}"   
 # 1 equipment can have multiple sensor readings, 
 # but each sensor reading belongs to one equipment.

  