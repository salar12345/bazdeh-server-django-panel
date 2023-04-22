from django.urls import path

from bzsdp.app.api.controller.content.education.education_lis_controller import EducationListController
from bzsdp.app.api.controller.content.education.education_single_controller import EducationSingleController

urlpatterns = [
    path("list/", EducationListController.as_view()),
    path("single/", EducationSingleController.as_view())
]
