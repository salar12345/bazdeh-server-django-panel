from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ncl.utils.common.singleton import Singleton
from bzsdp.app.api.controller.base_api_view import BasePanelController
from bzsdp.app.api.serializer.interaction.news_analysis_like.news_analysis_like_request_serializer import NewsAnalysisLikeRequestSerializer

from bzsdp.app.logic.interaction.interaction_logic import InteractionLogic
from bzsdp.app.model.vo.interaction.news_analysis_like_vo import NewsAnalysisLikeVO


class NewsAnalysisDoDisLikeController(BasePanelController, APIView, metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.logic = InteractionLogic()

    def post(self, request):

        data = request.data
        member = self.get_current_member(request)

        serializer = NewsAnalysisLikeRequestSerializer(data=data)
        if serializer.is_valid():
            news_analysis_id = serializer.data.get(NewsAnalysisLikeVO.NEWS_ANALYSIS_ID)
            state = serializer.data.get(NewsAnalysisLikeVO.STATE)
            news_or_analysis = serializer.data.get(NewsAnalysisLikeVO.NEWS_OR_ANALYSIS)
            try:
                self.logic.do_dislike(news_analysis_id=news_analysis_id, member=member, state=state, news_or_analysis=news_or_analysis)

                return Response(status=status.HTTP_201_CREATED)
            except:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
