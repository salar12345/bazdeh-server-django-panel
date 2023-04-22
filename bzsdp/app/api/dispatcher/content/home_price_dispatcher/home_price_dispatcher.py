from django.urls import path

from bzsdp.app.api.controller.content.housing.housing_list_controller import GetListHomePriceController
from bzsdp.app.api.controller.content.housing.housing_single_controller import GetSingleHomePriceController
from bzsdp.app.api.controller.content.housing.start_and_end_time_housing_controller import \
    StartAndEndTimeHomePriceController

urlpatterns = [
    path("start_end_time", StartAndEndTimeHomePriceController.as_view()),
    path('list', GetListHomePriceController.as_view()),
    path('single', GetSingleHomePriceController.as_view())
]
