from django.urls import path

from bzsdp.app.api.controller.member.user_search_list_controller import UserSearchController


urlpatterns = [
    path('', UserSearchController.as_view())
]
