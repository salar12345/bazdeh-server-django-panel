from django.urls import path

from bzsdp.app.api.controller.member.profile.profile_editor_controller import ProfileEditorController
from bzsdp.app.api.controller.member.profile.profile_geter_controller import ProfileGeterController
from bzsdp.app.api.controller.member.profile.profile_image_controller import ProfileImageController

urlpatterns = [
    path("", ProfileGeterController.as_view()),
    path("/edit", ProfileEditorController.as_view()),
    path("/images", ProfileImageController.as_view())
]
