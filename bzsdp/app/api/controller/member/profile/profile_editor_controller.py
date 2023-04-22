from ncl.utils.common.singleton import Singleton
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from bzsdp.app.api.controller.base_api_view import BasePanelController
from bzsdp.app.api.serializer.member.portfolio.profile_editor_serializer import ProfileEditorSerializer
from bzsdp.app.logic.member.member_logic import MemberLogic
from bzsdp.app.model.vo.member.profile_vo import ProfileVO


class ProfileEditorController(BasePanelController, APIView, metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.logic = MemberLogic()

    def post(self, request):
        data = request.data
        member = self.get_current_member(request)
        serializer = ProfileEditorSerializer(data=data)
        if serializer.is_valid():
            name = serializer.data.get(ProfileVO.NAME)
            last_name = serializer.data.get(ProfileVO.LAST_NAME)
            image_url = serializer.data.get(ProfileVO.IMAGE_URL)
            try:
                self.logic.edit_profile(member=member, name=name, last_name=last_name, image_url=image_url)
                return Response(status=status.HTTP_201_CREATED)
            except:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

