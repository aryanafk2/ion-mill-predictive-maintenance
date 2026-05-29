from django.urls import path

from .views import (
    SensorReadingCreateView,
    EquipmentHealthView,
    RecentReadingsView,
    AlertsView,
    EquipmentListView,
    FleetHealthView,
)

urlpatterns = [
    # Telemetry ingestion
    path(
        "sensor-readings/",
        SensorReadingCreateView.as_view(),
        name="sensor-readings",
    ),

    # Latest equipment health
    path(
        "equipment/<int:equipment_id>/health/",
        EquipmentHealthView.as_view(),
        name="equipment-health",
    ),

    # Recent readings for charts
    path(
        "equipment/<int:equipment_id>/readings/",
        RecentReadingsView.as_view(),
        name="equipment-readings",
    ),

    # Active alerts
    path(
        "alerts/",
        AlertsView.as_view(),
        name="alerts",
    ),

    path(
        "equipment/",
        EquipmentListView.as_view(),
        name="equipment-list",
    ),

    path(
        "fleet-health/",
        FleetHealthView.as_view(),
        name="fleet-health",
    ),
]