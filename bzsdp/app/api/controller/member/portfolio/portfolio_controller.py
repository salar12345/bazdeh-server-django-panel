from ncl.utils.common.singleton import Singleton
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from bzsdp.app.api.controller.base_api_view import BasePanelController
from bzsdp.app.api.serializer.member.portfolio.portfolio_get_serializer import PortfolioGetSerializer
from bzsdp.app.api.serializer.member.portfolio.portfolio_request_serializer import PortfolioRequestSerializer
from bzsdp.app.api.serializer.member.portfolio.portfolio_response_serializer import PortfolioResponseSerializer

from bzsdp.app.logic.member.member_logic import MemberLogic
from bzsdp.app.model.vo.member.portfolio_vo import PortfolioVO


class PortfolioController(BasePanelController, APIView, metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.logic = MemberLogic()

    def get(self, request):
        member = self.get_current_member(request)
        try:
            all_portfolios = self.logic.get_portfolios(member=member)
            list_of_portfolio = []
            for portfolio in all_portfolios:
                result_dict = {}
                count_of_assets = self.logic.get_count_of_assets(portfolio=portfolio)
                result_dict[PortfolioVO.COUNT] = count_of_assets
                result_dict[PortfolioVO.ID] = portfolio.id
                result_dict[PortfolioVO.NAME] = portfolio.name
                list_of_portfolio.append(result_dict)

            serialized_result = PortfolioGetSerializer(data=list_of_portfolio, many=True)
            if serialized_result.is_valid():

                return Response(serialized_result.data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):

        data = request.data

        serializer = PortfolioRequestSerializer(data=data)
        member = self.get_current_member(request)

        if serializer.is_valid():
            name = serializer.data.get(PortfolioVO.NAME)
            portfolio_id = self.logic.add_portfolio_for_member(member=member,
                                                               name=name)
            portfolio_id_dict = {PortfolioVO.ID: portfolio_id}

            serialized_portfolio_id = PortfolioResponseSerializer(portfolio_id_dict)
            return Response(serialized_portfolio_id.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
