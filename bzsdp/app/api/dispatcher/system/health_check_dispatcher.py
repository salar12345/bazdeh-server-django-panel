from django.urls import path

from bzsdp.app.api.controller.system.health_check_controller import HealthCheckController

urlpatterns = [
    path('', HealthCheckController.as_view())
]
