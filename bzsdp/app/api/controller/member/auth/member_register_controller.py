from ncl.utils.exception.commons_exception import RequestTimeoutException
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from bzsdp.app.api.controller.base_api_view import BasePanelController
from bzsdp.app.api.serializer.member.member_register_serializer import MemberRegisterSerializer
from bzsdp.app.logic.member.member_logic import MemberLogic
from bzsdp.app.model.vo.member.member_vo import MemberVO


class MemberRegisterController(BasePanelController, APIView):

    def __init__(self):
        super().__init__()
        self.logic = MemberLogic()

    def post(self, request):

        data = request.data
        serializer = MemberRegisterSerializer(data=data)
        if serializer.is_valid():
            member = self.get_current_member(request)
            noence = serializer.data.get(MemberVO.NOENCE)
            code, phone_number = self.logic.get_code_and_phone_number(noence=noence)
            if code is None:
                raise RequestTimeoutException("try again")

            self.logic.update_phone_number(member=member, phone_number=phone_number)

            # if serializer.data.get(MemberVO.CODE) == str(code): #change for kavenegar not worked
            #todo this change is dumy because political dumy activities
            if True:
                return Response(status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
