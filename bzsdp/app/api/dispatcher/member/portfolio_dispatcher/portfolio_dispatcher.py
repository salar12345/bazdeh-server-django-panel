from django.urls import path

from bzsdp.app.api.controller.member.portfolio.delete_portfolio_controller import DeletePortfolioController
from bzsdp.app.api.controller.member.portfolio.portfolio_controller import PortfolioController
from bzsdp.app.api.controller.member.portfolio.serve_portfolio_controller import ServePortfolioController

urlpatterns = [
    path("", PortfolioController.as_view()),
    path("delete", DeletePortfolioController.as_view()),
    path("serve", ServePortfolioController.as_view()),
]
