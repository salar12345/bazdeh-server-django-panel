from django.urls import path
from bzsdp.app.api.controller.interaction.inflation_tracker.priceables_list_controller import PriceablesListController
from bzsdp.app.api.controller.interaction.inflation_tracker.inflation_rate_controller import InflationRateController
from bzsdp.app.api.controller.interaction.inflation_tracker.inflation_tracker_controller import InflationTrackerController


urlpatterns = [
    path('priceables-list/', PriceablesListController.as_view()),
    path('inflation-rate/', InflationRateController.as_view()),
    path('', InflationTrackerController.as_view())
]
