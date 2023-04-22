from ncl.utils.common.singleton import Singleton
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from bzsdp.app.api.controller.base_api_view import BasePanelController
from bzsdp.app.api.serializer.interaction.report_serializer import ReportSerializer
from bzsdp.app.logic.interaction.interaction_logic import InteractionLogic
from bzsdp.app.model.vo.interaction.interaction_vo import InteractionVO


class ReportController(BasePanelController, APIView, metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.logic = InteractionLogic()

    def post(self, request):
        report = request.data
        serializer = ReportSerializer(report)
        if serializer.is_valid():
            if self.logic.save_report(news_url=serializer.data.get(InteractionVO.NEWS_URL)):
                return Response(status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
