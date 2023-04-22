from ncl.utils.common.singleton import Singleton
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from bzsdp.app.api.controller.base_api_view import BasePanelController
from bzsdp.app.api.serializer.member.portfolio.delete_porfolio_serializer import DeletePortfolioSerializer
from bzsdp.app.logic.member.member_logic import MemberLogic
from bzsdp.app.model.vo.member.portfolio_vo import PortfolioVO


class DeletePortfolioController(BasePanelController, APIView, metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.logic = MemberLogic()

    def post(self, request):

        data = request.data

        serializer = DeletePortfolioSerializer(data=data)

        if serializer.is_valid():
            portfolio_id = serializer.data.get(PortfolioVO.ID)
            self.logic.delete_portfolio(portfolio_id=portfolio_id)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
