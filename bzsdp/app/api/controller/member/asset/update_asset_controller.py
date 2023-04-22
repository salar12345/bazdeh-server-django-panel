from ncl.utils.common.singleton import Singleton
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from bzsdp.app.api.controller.base_api_view import BasePanelController
from bzsdp.app.api.serializer.member.asset.update_asset_serializer import UpdateAssetSerializer
from bzsdp.app.logic.member.member_logic import MemberLogic
from bzsdp.app.model.vo.member.asset_vo import AssetVO


class UpdateAssetController(BasePanelController, APIView, metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.logic = MemberLogic()

    def post(self, request):

        data = request.data

        serializer = UpdateAssetSerializer(data=data)

        if serializer.is_valid():
            asset_id = serializer.data.get(AssetVO.ID)
            asset_by_id = self.logic.get_asset_by_id(asset_id=asset_id)

            name = serializer.data.get(AssetVO.NAME)
            if name is None:
                name = asset_by_id[0].name

            code = serializer.data.get(AssetVO.CODE)
            if code is None:
                code = asset_by_id[0].code

            count = serializer.data.get(AssetVO.COUNT)
            if count is None:
                count = asset_by_id[0].count

            buy_price = serializer.data.get(AssetVO.BUY_PRICE)
            if buy_price is None:
                buy_price = asset_by_id[0].buy_price

            daily_usd_price = serializer.data.get(AssetVO.DAILY_USD_PRICE, None)
            if daily_usd_price is None:
                daily_usd_price = asset_by_id[0].daily_usd_price

            date_time = serializer.data.get(AssetVO.DATE_TIME, None)
            if date_time is None:
                date_time = asset_by_id[0].date_time

            description = serializer.data.get(AssetVO.DESCRIPTION, None)
            if description is None:
                description = asset_by_id[0].description
            self.logic.update_asset(asset_id=asset_id, name=name, code=code, count=count, buy_price=buy_price,
                                    daily_usd_price=daily_usd_price, date_time=date_time, description=description)

            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
