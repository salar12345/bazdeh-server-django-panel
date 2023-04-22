from django.urls import path

from bzsdp.app.api.controller.content.web_post.single_web_post_controller import SingleWebPostController
from bzsdp.app.api.controller.content.web_post.list_web_post_controller import ListWebPostController

urlpatterns = [
    path('single/', SingleWebPostController.as_view()),
    path('query/', ListWebPostController.as_view())
]
