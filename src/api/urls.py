from django.urls import path
from .views import LatencyView

urlpatterns = [
    path("latency/", LatencyView.as_view(), name="latency"),
]
