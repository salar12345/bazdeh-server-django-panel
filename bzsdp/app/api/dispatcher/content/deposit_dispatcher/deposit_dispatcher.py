from django.urls import path

from bzsdp.app.api.controller.content.deposit.deposit_list_controller import DepositListController
from bzsdp.app.api.controller.content.deposit.related_deposit_controller import RelatedDepositController
from bzsdp.app.api.controller.content.deposit.single_deposit_controller import SingleDepositController

urlpatterns = [
    path("list", DepositListController.as_view()),
    path("single", SingleDepositController.as_view()),
    path("related", RelatedDepositController.as_view())

]
