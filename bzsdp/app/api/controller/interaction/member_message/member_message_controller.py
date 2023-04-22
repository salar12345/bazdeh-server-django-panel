from ncl.utils.common.singleton import Singleton
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from bzsdp.app.api.controller.base_api_view import BasePanelController
from bzsdp.app.api.serializer.interaction.member_message_serializer import MemberMessageSerializer
from bzsdp.app.logic.interaction.interaction_logic import InteractionLogic


class MemberMessageController(BasePanelController, APIView, metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.logic = InteractionLogic()

    def post(self, request):
        message = request.data
        serializer = MemberMessageSerializer(data=message)
        if serializer.is_valid():
            member = self.get_current_member(request=request)
            if self.logic.save_reported_message(serializer.data, member=member):
                return Response(status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


