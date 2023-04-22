
from django.urls import path

from bzsdp.app.api.controller.content.special_pages.special_page_controller import SpecialPageController

urlpatterns = [
    path("special_page/", SpecialPageController.as_view())
]


