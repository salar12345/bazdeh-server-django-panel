from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ncl.utils.common.singleton import Singleton
from bzsdp.app.api.controller.base_api_view import BasePanelController

from bzsdp.app.api.serializer.interaction.news_analysis_read.news_analysis_read_serializer import NewsAnalysisReadSerializer
from bzsdp.app.logic.interaction.interaction_logic import InteractionLogic
from bzsdp.app.model.vo.interaction.interaction_vo import InteractionVO


class NewsAnalysisReadController(BasePanelController, APIView, metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.logic = InteractionLogic()

    def post(self, request):

        data = request.data
        member = self.get_current_member(request)

        serializer = NewsAnalysisReadSerializer(data=data)
        if serializer.is_valid():
            news_analysis_id = serializer.data.get(InteractionVO.NEWS_ANALYSIS_ID)
            news_or_analysis = serializer.data.get(InteractionVO.NEWS_OR_ANALYSIS)
            try:
                self.logic.add_news_or_analysis_to_has_been_read_entity(member=member,
                                                                        news_or_analysis=news_or_analysis,
                                                                        news_or_analysis_id=news_analysis_id)
                return Response(status=status.HTTP_201_CREATED)
            except:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


