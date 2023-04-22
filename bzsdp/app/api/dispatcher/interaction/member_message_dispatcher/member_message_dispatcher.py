from django.urls import path

from bzsdp.app.api.controller.interaction.member_message.member_message_controller import MemberMessageController

urlpatterns = [
    path('reported_error/', MemberMessageController.as_view())
]