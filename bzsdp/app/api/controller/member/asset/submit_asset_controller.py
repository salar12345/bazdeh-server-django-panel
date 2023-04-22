from ncl.utils.common.singleton import Singleton
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from bzsdp.app.api.controller.base_api_view import BasePanelController
from bzsdp.app.api.serializer.member.asset.asset_id_serializer import AssetIDSerializer
from bzsdp.app.api.serializer.member.asset.asset_serializer import AssetSerializer
from bzsdp.app.logic.member.member_logic import MemberLogic
from bzsdp.app.model.vo.member.asset_vo import AssetVO


class SubmitAssetController(BasePanelController, APIView, metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.logic = MemberLogic()

    def post(self, request):

        data = request.data
        member = self.get_current_member(request)
        serializer = AssetSerializer(data=data)

        if serializer.is_valid():
            name = serializer.data.get(AssetVO.NAME)
            code = serializer.data.get(AssetVO.CODE)
            parent_code = serializer.data.get(AssetVO.PARENT_CODE)
            portfolio_id = serializer.data.get(AssetVO.PORTFOLIO_ID)
            company_name = serializer.data.get(AssetVO.COMPANY_NAME)
            count = serializer.data.get(AssetVO.COUNT)
            buy_price = serializer.data.get(AssetVO.BUY_PRICE)
            date_time = serializer.data.get(AssetVO.DATE_TIME)
            date_time = date_time + AssetVO.DATE_FORMAT
            description = serializer.data.get(AssetVO.DESCRIPTION)
            daily_usd_price = serializer.data.get(AssetVO.DAILY_USD_PRICE)
            base_value = serializer.data.get(AssetVO.BASE_VALUE)
            asset_id = self.logic.save_details_of_asset(member=member, name=name, code=code,
                                                        parent_code=parent_code,
                                                        portfolio_id=portfolio_id,
                                                        company_name=company_name, count=count,
                                                        buy_price=buy_price, date_time=date_time,
                                                        description=description,
                                                        daily_usd_price=daily_usd_price,
                                                        base_value=base_value)
            asset_id_dict = {AssetVO.ID: asset_id}

            serialized_asset_id = AssetIDSerializer(asset_id_dict)
            return Response(serialized_asset_id.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
