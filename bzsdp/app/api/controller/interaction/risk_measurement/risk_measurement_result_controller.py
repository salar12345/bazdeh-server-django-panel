from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from bzsdp.app.api.controller.base_api_view import BasePanelController
from bzsdp.app.logic.interaction.risk_measurement_logic import RiskMeasurementLogic


class RiskMeasurementResultController(APIView, BasePanelController):
    def __init__(self, **kwargs):
        self.risk_measuerment_logic = RiskMeasurementLogic()
        super().__init__(**kwargs)

    def get(self, request: Request) -> Response:
        try:
            return Response(self.risk_measuerment_logic.get_result(self.get_current_member(request)), HTTP_200_OK)
        except Exception:
            return Response(None, HTTP_400_BAD_REQUEST)
