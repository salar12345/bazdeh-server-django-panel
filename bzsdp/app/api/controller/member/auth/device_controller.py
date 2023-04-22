from django.contrib.auth.models import AnonymousUser
from ncl.utils.common.singleton import Singleton
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from bzsdp.app.api.controller.base_api_view import BasePanelController
from bzsdp.app.api.serializer.member.device_serializer import DeviceSerializer
from bzsdp.app.logic.member.device_logic import DeviceLogic
from bzsdp.app.logic.member.member_logic import MemberLogic


class DeviceController(BasePanelController, APIView, metaclass=Singleton):

    def __init__(self):
        super().__init__()

        self.logic = DeviceLogic()
        self.member_logic = MemberLogic()

    def post(self, request):
        device = request.data
        serializer = DeviceSerializer(data=device)
        member = self.get_current_member(request=request)
        if member is AnonymousUser:
            return Response(status=status.HTTP_403_FORBIDDEN)

        if serializer.is_valid():

            device = self.logic.save_or_update_davice_info(device_info=serializer.data)

            if device:
                self.member_logic.create_member_device_relation(device=device, member=member)

                return Response(status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
