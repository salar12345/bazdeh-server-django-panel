from bzsdp.app.api.controller.base_api_view import BasePanelController
from bzsdp.app.api.serializer.interaction.inflation_tracker.inflation_tracker_serializer import InflationTrackerSerializer
from bzsdp.app.api.serializer.interaction.inflation_tracker.inflation_tracker_result_serializer import InflationTrackerResultSerializer
from bzsdp.app.logic.interaction.inflation_tracker.inflation_tracker_logic import InflationTrackerLogic
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from ncl.utils.common.singleton import Singleton
from bzsdp.app.model.vo.interaction.inflation_tracker_vo import InflationTrackerVO


class InflationTrackerController(BasePanelController, APIView, metaclass=Singleton):

    def __init__(self):
        super().__init__()
        self.logic = InflationTrackerLogic()

    def get(self, request: Request) -> Response:
        try:
            serializer = InflationTrackerSerializer(data=request.query_params)
            serializer.is_valid(raise_exception=True)

            priceable_id = serializer.data.get(InflationTrackerVO.PRICEABLE_ID)

            inflation_tracker_info = self.logic.get_inflation_tracker_info(priceable_id)
            serializer = InflationTrackerResultSerializer(inflation_tracker_info)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as exc:
            return Response(exc, status=status.HTTP_400_BAD_REQUEST)
