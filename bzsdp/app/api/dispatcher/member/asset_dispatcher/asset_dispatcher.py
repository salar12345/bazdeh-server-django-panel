from django.urls import path

from bzsdp.app.api.controller.member.asset.get_asset_controller import GetAssetController
from bzsdp.app.api.controller.member.asset.delete_asset_controller import DeleteAssetController
from bzsdp.app.api.controller.member.asset.submit_asset_controller import SubmitAssetController
from bzsdp.app.api.controller.member.asset.update_asset_controller import UpdateAssetController

urlpatterns = [
    path("", GetAssetController.as_view()),
    path("submit", SubmitAssetController.as_view()),
    path("delete", DeleteAssetController.as_view()),
    path("update", UpdateAssetController.as_view()),
]
