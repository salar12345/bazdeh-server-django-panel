from django.urls import path

from bzsdp.app.api.controller.system.startup_controller import StartupController

urlpatterns = [
    path('', StartupController.as_view()),
]
