from bzsdp.app.api.controller.base_api_view import BasePanelController
from bzsdp.app.logic.interaction.inflation_tracker.inflation_rate_logic import InflationRateLogic
from bzsdp.app.api.serializer.interaction.inflation_tracker.inflation_rate_serialzier import InflationRateSerializer
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from ncl.utils.common.singleton import Singleton


class InflationRateController(BasePanelController, APIView, metaclass=Singleton):

    def __init__(self):
        super().__init__()
        self.logic = InflationRateLogic()

    def get(self, request: Request) -> Response:
        try:
            inflation_rate_list = self.logic.get_inflation_rate_list()
            serializer = InflationRateSerializer(inflation_rate_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as exc:
            return Response(exc, status=status.HTTP_400_BAD_REQUEST)
