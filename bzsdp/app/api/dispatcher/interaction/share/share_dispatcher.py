from django.urls import path
from bzsdp.app.api.controller.interaction.share.share_calculator_controller import ShareCalculatorsController


urlpatterns = [
    path('', ShareCalculatorsController.as_view()),
]
