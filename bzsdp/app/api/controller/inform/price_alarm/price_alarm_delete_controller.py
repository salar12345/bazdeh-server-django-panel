from ncl.utils.common.singleton import Singleton
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from bzsdp.app.api.controller.base_api_view import BasePanelController
from bzsdp.app.api.serializer.inform.alarm.delete_alarm_serializer import DeleteAlarmSerializer
from bzsdp.app.logic.inform.alarm_logic import AlarmLogic
from bzsdp.app.model.vo.inform.alarm_price_vo import AlarmPriceVO


class PriceAlarmDeleteController(BasePanelController, APIView, metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.logic = AlarmLogic()

    def post(self, request):
        data = request.data
        serializer = DeleteAlarmSerializer(data=data)
        if serializer.is_valid():
            alarm_id = serializer.data.get(AlarmPriceVO.ALARM_ID)

            self.logic.delete_alarm(alarm_id=alarm_id)

            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
