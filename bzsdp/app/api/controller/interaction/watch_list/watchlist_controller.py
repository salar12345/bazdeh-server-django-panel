
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from bzsdp.app.api.controller.base_api_view import BasePanelController

from bzsdp.app.api.serializer.interaction.watchlist_serializer import WatchlistSerializer, \
    WatchListSerializer
from bzsdp.app.logic.interaction.interaction_logic import InteractionLogic

from bzsdp.app.model.vo.interaction.watchlist_vo import WatchlistVO


class WatchlistController(BasePanelController, APIView):

    def __init__(self):
        super().__init__()
        self.logic = InteractionLogic()

    def get(self, request):

        try:
            member = self.get_current_member(request)
            all_watch_list = self.logic.get_all_watchlist_entity(member=member)

            serialized_watch_lists = WatchListSerializer(all_watch_list, many=True)
            return Response(serialized_watch_lists.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):

        data = request.data

        serializer = WatchlistSerializer(data=data)
        member = self.get_current_member(request)
        if serializer.is_valid():
            code = serializer.data.get(WatchlistVO.ITEM_CODE)
            parent_code = serializer.data.get(WatchlistVO.PARENT_CODE)
            self.logic.save_code_to_watchlist_in_watchlist_entity(code=code, member=member,
                                                                  parent_code=parent_code)

            return Response(status=status.HTTP_201_CREATED)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
