from ncl.utils.exception.commons_exception import ExternalServiceNotAvailableException
from ncl.utils.common.singleton import Singleton
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from bzsdp.app.api.controller.base_api_view import BasePanelController
from bzsdp.app.api.serializer.member.member_login_serializer import MemberLoginSerializer
from bzsdp.app.logic.member.member_logic import MemberLogic
from bzsdp.app.model.vo.member.member_vo import MemberVO
from bzsdp.app.shared.adapter.kavenegar_sms_adapter import KaveNegarService


class MemberLoginController(BasePanelController, APIView, metaclass=Singleton):

    def __init__(self):
        super().__init__()
        self.logic = MemberLogic()

    def post(self, request, format=None):
        data = request.data
        serializer = MemberLoginSerializer(data=data)
        if serializer.is_valid():
            code, noence = self.logic.create_code_and_noence()
            phone_number = serializer.data.get(MemberVO.PHONE_NUMBER)
            self.logic.cache_code_and_noence(code=code, noence=noence, phone_number=phone_number)
            member = self.logic.find_member_by_phone_number(phone_number=phone_number)
            access_token = None
            refresh_token = None
            if member:
                refresh_token, access_token = self.logic.generate_member_token(member=member)

            try:
                kave_negar_response = KaveNegarService().send_sms(phone_number=phone_number, code=code)
                if kave_negar_response[0][MemberVO.STATUS] != 5:
                    raise ExternalServiceNotAvailableException("SMS provider error")

                else:
                    if refresh_token is None and access_token is None:
                        result = {MemberVO.NOENCE: noence, MemberVO.ACCESS_TOKEN: access_token,
                                  MemberVO.REFRESH_TOKEN: refresh_token}
                    else:
                        result = {MemberVO.NOENCE: noence, MemberVO.ACCESS_TOKEN: str(access_token),
                                  MemberVO.REFRESH_TOKEN: str(refresh_token)}

                    return Response(result, status=status.HTTP_201_CREATED)

            except:
                raise ExternalServiceNotAvailableException("SMS provider error")

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
