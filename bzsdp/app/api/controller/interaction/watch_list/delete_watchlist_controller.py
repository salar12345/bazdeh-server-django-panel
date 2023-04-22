
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from bzsdp.app.api.controller.base_api_view import BasePanelController

from bzsdp.app.api.serializer.interaction.watchlist_serializer import WatchlistSerializer

from bzsdp.app.logic.interaction.interaction_logic import InteractionLogic

from bzsdp.app.model.vo.interaction.watchlist_vo import WatchlistVO


class DeleteWatchlistController(BasePanelController, APIView):

    def __init__(self):
        super().__init__()
        self.logic = InteractionLogic()

    def post(self, request):

        data = request.data

        serializer = WatchlistSerializer(data=data)
        member = self.get_current_member(request)

        if serializer.is_valid():
            one_item_in_watchlist_code = serializer.data.get(WatchlistVO.ITEM_CODE)
            self.logic.delete_item_from_watchlist_entity(member=member,
                                                                   one_item_in_watchlist_code=one_item_in_watchlist_code)

            return Response(status=status.HTTP_200_OK)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


