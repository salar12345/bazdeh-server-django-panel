from django.urls import path

from bzsdp.app.api.controller.content.loan.loan_calculator_controller import LoanCalculatorController
from bzsdp.app.api.controller.content.loan.loan_controller import LoanController
from bzsdp.app.api.controller.content.loan.single_loan_controller import SingleLoanController

urlpatterns = [
    path("loan_group", LoanController.as_view()),
    path("loan_calculator", LoanCalculatorController.as_view()),
    path("loan_single", SingleLoanController.as_view())
]
