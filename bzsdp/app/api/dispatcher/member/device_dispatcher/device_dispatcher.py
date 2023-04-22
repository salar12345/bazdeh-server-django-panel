from django.urls import path

from bzsdp.app.api.controller.member.auth.device_controller import DeviceController

urlpatterns = [
    path('submit_device/', DeviceController.as_view())
]
