from django.urls import path

from bzsdp.app.api.controller.content.car.car_historical_price_controller import CarHistoricalPriceController
from bzsdp.app.api.controller.content.car.car_last_price_controller import CarLastPriceController
from bzsdp.app.api.controller.content.car.car_single_controller import CarSingleController


urlpatterns = [
    path('price_list', CarLastPriceController.as_view()),
    path('<str:id>/', CarSingleController.as_view())

    # path("chart", CarHistoricalPriceController.as_view())
]
