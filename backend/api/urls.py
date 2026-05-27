from django.urls import path
from .views import SensorReadingCreateView

urlpatterns = [
    path(
        'sensor-readings/',
        SensorReadingCreateView.as_view(),
        name='sensor-readings'
    ),
]
