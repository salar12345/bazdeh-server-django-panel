from ncl.utils.common.singleton import Singleton
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from bzsdp.app.api.controller.base_api_view import BasePanelController
from bzsdp.app.api.serializer.inform.alarm.get_by_name_alarm_request_serializer import GetByNameAlarmRequestSerializer
from bzsdp.app.api.serializer.inform.alarm.get_by_name_alarm_response_serializer import GetByNameAlarmsResponseSerializer
from bzsdp.app.logic.inform.alarm_logic import AlarmLogic
from bzsdp.app.model.vo.inform.alarm_price_vo import AlarmPriceVO


class PriceAlarmGetByNameController(BasePanelController, APIView, metaclass=Singleton):

    def __init__(self):
        super().__init__()
        self.logic = AlarmLogic()

    def post(self, request):

        member = self.get_current_member(request)
        data = request.data
        serializer = GetByNameAlarmRequestSerializer(data=data)
        if serializer.is_valid():
            code = serializer.data.get(AlarmPriceVO.CODE)
            by_name_alarms = self.logic.get_by_name_alarms(member=member, code=code)
            try:
                serialized_result = GetByNameAlarmsResponseSerializer(by_name_alarms, many=True)
                return Response(serialized_result.data, status=status.HTTP_200_OK)
            except:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
