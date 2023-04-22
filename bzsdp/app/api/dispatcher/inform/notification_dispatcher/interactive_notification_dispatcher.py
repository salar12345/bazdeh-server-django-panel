from django.urls import path

from bzsdp.app.api.controller.inform.notification.interactive_notification_controller import \
    InteractiveNotificationController

urlpatterns = [
    path('', InteractiveNotificationController.as_view())
]
