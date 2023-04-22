from django.urls import path

from bzsdp.app.api.controller.interaction.risk_measurement.risk_measurement_controller import RiskMeasurementController
from bzsdp.app.api.controller.interaction.risk_measurement.risk_measurement_result_controller import \
    RiskMeasurementResultController

urlpatterns = [
    path('', RiskMeasurementController.as_view()),
    path('result/', RiskMeasurementResultController.as_view())
]
