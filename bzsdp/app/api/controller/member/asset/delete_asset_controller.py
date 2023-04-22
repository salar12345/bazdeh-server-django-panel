from ncl.utils.common.singleton import Singleton
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from bzsdp.app.api.controller.base_api_view import BasePanelController
from bzsdp.app.api.serializer.member.asset.delete_asset_serializer import DeleteAssetSerializer
from bzsdp.app.logic.member.member_logic import MemberLogic
from bzsdp.app.model.vo.member.portfolio_vo import PortfolioVO


class DeleteAssetController(BasePanelController, APIView, metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.logic = MemberLogic()

    def post(self, request):

        data = request.data
        serializer = DeleteAssetSerializer(data=data)
        if serializer.is_valid():
            asset_id = serializer.data.get(PortfolioVO.ID)
            self.logic.delete_asset(asset_id=asset_id)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
