from django.urls import path

from bzsdp.app.api.controller.member.auth.member_login_controller import MemberLoginController
from bzsdp.app.api.controller.member.auth.member_register_controller import MemberRegisterController
from bzsdp.app.api.controller.member.auth.v1_token_refresh_controller import V1TokenRefreshController

urlpatterns = [
    path('login', MemberLoginController.as_view()),
    path('register', MemberRegisterController.as_view()),
    path('refresh', V1TokenRefreshController.as_view())
]
