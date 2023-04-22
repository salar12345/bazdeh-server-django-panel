from ncl.utils.common.singleton import Singleton
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from bzsdp.app.api.controller.base_api_view import BasePanelController
from bzsdp.app.api.serializer.inform.alarm.set_price_alarm_serializer import SetPriceAlarmSerializer
from bzsdp.app.logic.inform.alarm_logic import AlarmLogic
from bzsdp.app.model.vo.inform.alarm_price_vo import AlarmPriceVO


class PriceAlarmSetController(BasePanelController, APIView, metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.logic = AlarmLogic()

    def post(self, request):
        member = self.get_current_member(request)
        data = request.data
        serializer = SetPriceAlarmSerializer(data=data)
        if serializer.is_valid():
            alarm_price = serializer.data.get(AlarmPriceVO.ALARM_PRICE)
            now_price = serializer.data.get(AlarmPriceVO.NOW_PRICE)
            name = serializer.data.get(AlarmPriceVO.NAME)
            code = serializer.data.get(AlarmPriceVO.CODE)
            parent_code = serializer.data.get(AlarmPriceVO.PARENT_CODE)
            is_repeated = serializer.data.get(AlarmPriceVO.IS_REPEATED)
            is_notify = serializer.data.get(AlarmPriceVO.IS_NOTIFY)

            self.logic.set_price_alarm(member=member, alarm_price=alarm_price, now_price=now_price, name=name,
                                       code=code, parent_code=parent_code, is_repeated=is_repeated, is_notify=is_notify)

            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
