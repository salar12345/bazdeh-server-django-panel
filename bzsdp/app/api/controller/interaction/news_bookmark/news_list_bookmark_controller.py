from ncl.utils.common.singleton import Singleton
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from bzsdp.app.api.controller.base_api_view import BasePanelController
from bzsdp.app.logic.interaction.interaction_logic import InteractionLogic
from bzsdp.app.model.vo.interaction.interaction_vo import InteractionVO


class NewsListBookmarkController(BasePanelController, APIView, metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.logic = InteractionLogic()

    def get(self, request):
        member = self.get_current_member(request)
        try:
            bookmark_id_list = self.logic.get_bookmark_id_list(member=member)
            bookmark_news_id_list = [x.get(InteractionVO.NEWS_ID) for x in bookmark_id_list]
            return Response(bookmark_news_id_list, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
