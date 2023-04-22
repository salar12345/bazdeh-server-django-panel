from ncl.utils.common.singleton import Singleton
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from bzsdp.app.api.controller.base_api_view import BasePanelController
from bzsdp.app.api.serializer.member.profile.profile_image_serializer import ProfileImageSerializer

from bzsdp.app.logic.member.member_logic import MemberLogic


class ProfileImageController(BasePanelController, APIView, metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.logic = MemberLogic()

    def get(self, request):
        try:
            profile_images = self.logic.get_profile_images()
            serialized_result = ProfileImageSerializer(data=profile_images, many=True)
            try:
                return Response(serialized_result.initial_data, status=status.HTTP_200_OK)
            except:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)