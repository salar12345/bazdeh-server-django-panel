from django.urls import path

from bzsdp.app.api.controller.content.home_page.home_page_controller import HomePageController

urlpatterns = [
    path("home_page/", HomePageController.as_view())
]
