from ncl.utils.common.singleton import Singleton
from rest_framework import status
from rest_framework.response import Response

from rest_framework.views import APIView

from bzsdp.app.adapter.grpc.post_serve.web_post_serve_adapter import WebPostServeAdapter
from bzsdp.app.api.controller.base_api_view import BasePanelController
from bzsdp.app.api.serializer.interaction.bookmark_serializer import BookmarkSerializer
from bzsdp.app.logic.interaction.interaction_logic import InteractionLogic
from bzsdp.app.model.vo.interaction.interaction_vo import InteractionVO


class NewsBookmarkController(BasePanelController, APIView, metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.logic = InteractionLogic()
        self.adapter = WebPostServeAdapter()

    def post(self, request):
        member = self.get_current_member(request)
        news_id = request.data
        serializer = BookmarkSerializer(data=news_id)

        if serializer.is_valid():
            try:
                if self.logic.add_news_bookmark(member=member, news_id=serializer.data[InteractionVO.NEWS_ID]):
                    return Response(status=status.HTTP_201_CREATED)
                else:
                    Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
            except Exception as e:
                print(e)
                return Response(status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        member = self.get_current_member(request)
        try:
            bookmark_id_list = self.logic.get_bookmark_id_list(member=member)
            bookmark_news_id_list = [x.get(InteractionVO.NEWS_ID) for x in bookmark_id_list]
            news_info_list = self.adapter.get_post_by_uri_list(uri_list=bookmark_news_id_list)
            return Response(news_info_list, status=status.HTTP_200_OK)
        except Exception:
            return Response(status=status.HTTP_404_NOT_FOUND)
