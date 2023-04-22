from rest_framework.response import Response
from rest_framework.views import APIView

from bzsdp.app.api.controller.base_api_view import BasePanelController
from bzsdp.app.logic.member.member_logic import MemberLogic
from bzsdp.app.model.vo.member.member_vo import MemberVO
from rest_framework import status

from bzsdp.app.model.vo.system.system_vo import SystemVO


class MemberRefreshController(BasePanelController, APIView):

    def __init__(self):
        super().__init__()
        self.logic = MemberLogic()

    def post(self, request):

        header = request.headers.get(SystemVO.AUTHORIZATION)
        try:
            access_token = self.logic.generate_access_token(refresh_token=header)
            result = {MemberVO.ACCESS_TOKEN: str(access_token)}
            return Response(result, status=status.HTTP_201_CREATED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
