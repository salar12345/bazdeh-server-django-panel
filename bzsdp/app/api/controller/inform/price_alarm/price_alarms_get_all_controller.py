from ncl.utils.common.singleton import Singleton
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from bzsdp.app.api.controller.base_api_view import BasePanelController
from bzsdp.app.api.serializer.inform.alarm.get_by_name_alarm_response_serializer import GetByNameAlarmsResponseSerializer
from bzsdp.app.logic.inform.alarm_logic import AlarmLogic


class PriceAlarmGetAllController(BasePanelController, APIView, metaclass=Singleton):

    def __init__(self):
        super().__init__()
        self.logic = AlarmLogic()

    def get(self, request):
        member = self.get_current_member(request)
        try:
            all_alarms = self.logic.get_all_alarms(member=member)

            try:
                serialized_result = GetByNameAlarmsResponseSerializer(all_alarms, many=True)
                return Response(serialized_result.data, status=status.HTTP_200_OK)
            except:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
