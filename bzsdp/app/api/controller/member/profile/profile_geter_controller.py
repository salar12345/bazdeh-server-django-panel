from ncl.utils.common.singleton import Singleton
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from bzsdp.app.api.controller.base_api_view import BasePanelController
from bzsdp.app.api.serializer.member.profile.profile_geter_serializer import GetProfileSerializer

from bzsdp.app.logic.member.member_logic import MemberLogic


class ProfileGeterController(BasePanelController, APIView, metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.logic = MemberLogic()

    def get(self, request):
        member = self.get_current_member(request)
        try:
            member_profile = self.logic.get_profile_by_member(member=member)
            serialized_result = GetProfileSerializer(member_profile)
            try:
                return Response(serialized_result.data, status=status.HTTP_200_OK)
            except:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
