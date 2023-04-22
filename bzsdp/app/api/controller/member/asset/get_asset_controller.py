from ncl.utils.common.singleton import Singleton
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from bzsdp.app.api.controller.base_api_view import BasePanelController
from bzsdp.app.api.serializer.member.asset.get_asset_response_serializer import GetAssetResponseSerializer
from bzsdp.app.api.serializer.member.asset.get_asset_request_serializer import GetAssetSerializer
from bzsdp.app.logic.member.member_logic import MemberLogic
from bzsdp.app.model.vo.member.asset_vo import AssetVO


class GetAssetController(BasePanelController, APIView, metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.logic = MemberLogic()

    def post(self, request):
        data = request.data
        member = self.get_current_member(request)
        serializer = GetAssetSerializer(data=data)
        if serializer.is_valid():
            portfolio_id = serializer.data.get(AssetVO.PORTFOLIO_ID)
            assets_by_portfolio_id_and_member_id = self.logic.get_assets_by_portfolio(
                portfolio_id=portfolio_id, member=member)

            serialized_result = GetAssetResponseSerializer(assets_by_portfolio_id_and_member_id, many=True)
            try:

                return Response(serialized_result.data, status=status.HTTP_200_OK)
            except:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

