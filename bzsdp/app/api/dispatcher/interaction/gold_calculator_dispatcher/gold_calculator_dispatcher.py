from django.urls import path

from bzsdp.app.api.controller.interaction.tool.gold_calculator_controller import GoldCalculatorController

urlpatterns = [
    path('gold_calculator/', GoldCalculatorController.as_view())
]