from ncl.utils.common.singleton import Singleton
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from bzsdp.app.api.controller.base_api_view import BasePanelController
from bzsdp.app.api.serializer.interaction.comment.news_or_analysis_comments_request_serializer import \
    NewsOrAnalysisCommentsRequestSerializer
from bzsdp.app.api.serializer.interaction.comment.news_or_analysis_comments_response_serializer import \
    NewsOrAnalysisCommentsResponseSerializer

from bzscl.model.vo.interaction.comment_vo import CommentVo

from bzsdp.app.logic.interaction.comment_logic import CommentLogic

class NewsOrAnalysisCommentsController(BasePanelController, APIView, metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.logic = CommentLogic()

    def post(self, request):
        data = request.data
        member = self.get_current_member(request)
        serializer = NewsOrAnalysisCommentsRequestSerializer(data=data)
        if serializer.is_valid():
            news_or_analysis_id = serializer.data.get(CommentVo.NEWS_OR_ANALYSIS_ID)

            try:
                news_or_analysis_comments = self.logic.get_news_or_analysis_comments(member=member,
                                                                                     news_or_analysis_id=news_or_analysis_id)

                serialized_response = NewsOrAnalysisCommentsResponseSerializer(news_or_analysis_comments, many=True)

                return Response(serialized_response.data, status=status.HTTP_200_OK)
            except:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
