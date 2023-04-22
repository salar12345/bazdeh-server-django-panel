from ncl.utils.common.singleton import Singleton
from rest_framework.views import APIView

from bzsdp.app.api.controller.base_api_view import BasePanelController
from bzsdp.app.api.serializer.content.special_news.special_news_serializer import SpecialNewsSerializer

from rest_framework.response import Response
from rest_framework import status

from bzsdp.app.logic.content.special_page_logic import SpecialPageLogic


class SpecialPageController(BasePanelController, APIView, metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.logic = SpecialPageLogic()

    def post(self, request):
        data = request.data

        serializer = SpecialNewsSerializer(data=data)

        if serializer.is_valid():
            news_list = self.logic.get_news_post(date_time=serializer.data['last_news_datetime'],
                                                 page=serializer.data['page_number'],
                                                 topic_in=[serializer.data['category']])

            return Response(news_list, status=status.HTTP_200_OK)
