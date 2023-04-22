from ncl.utils.common.singleton import Singleton

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from bzsdp.app.api.controller.base_api_view import BasePanelController
from bzsdp.app.api.serializer.interaction.bookmark_serializer import BookmarkSerializer
from bzsdp.app.logic.interaction.interaction_logic import InteractionLogic
from bzsdp.app.model.vo.interaction.interaction_vo import InteractionVO


class NewsBookmarkDeleteController(BasePanelController, APIView, metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.logic = InteractionLogic()

    def post(self, request):
        member = self.get_current_member(request)
        news_id = request.data
        serializer = BookmarkSerializer(data=news_id)
        if serializer.is_valid():
            try:
                if self.logic.delete_news_bookmark(member=member, news_id=serializer.data[InteractionVO.NEWS_ID]):
                    return Response(status=status.HTTP_200_OK)
                else:
                    return Response(status=status.HTTP_404_NOT_FOUND)
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
