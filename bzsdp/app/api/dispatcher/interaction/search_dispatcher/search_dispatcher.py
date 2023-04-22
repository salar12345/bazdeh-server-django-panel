from django.urls import path

from bzsdp.app.api.controller.interaction.search.deposit_search_controller import DepositSearchController
from bzsdp.app.api.controller.interaction.search.search_news_controller import SearchNewsController
from bzsdp.app.api.controller.interaction.search.search_analysis_controller import SearchAnalysisController
from bzsdp.app.api.controller.interaction.search.search_car_controller import SearchCarController
from bzsdp.app.api.controller.interaction.search.search_loan_controller import SearchLoanController
from bzsdp.app.api.controller.interaction.search.search_symbol_controller import SearchSymbolController


urlpatterns = [
    path('news/', SearchNewsController.as_view()),
    path('analysis/', SearchAnalysisController.as_view()),
    path('car/', SearchCarController.as_view()),
    path('loan/', SearchLoanController.as_view()),
    path('symbol/', SearchSymbolController.as_view()),
    path('deposit/', DepositSearchController.as_view())
]
