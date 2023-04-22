from django.urls import path

from bzsdp.app.api.controller.member.auth.member_exit_controller import MemberExitController

urlpatterns = [
    path('', MemberExitController.as_view())
]
