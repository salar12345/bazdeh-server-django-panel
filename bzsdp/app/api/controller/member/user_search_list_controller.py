from ncl.utils.common.singleton import Singleton
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from bzsdp.app.api.controller.base_api_view import BasePanelController
from bzsdp.app.api.serializer.member.get_user_search_list_serializer import GetUserSearchListSerializer
from bzsdp.app.api.serializer.member.serve_user_search_list_serializer import ServeUserSearchListSerializer

from bzsdp.app.logic.member.member_logic import MemberLogic
from bzsdp.app.model.vo.member.user_search_vo import UserSearchVO


class UserSearchController(BasePanelController, APIView, metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.logic = MemberLogic()

    def get(self, request):
        member = self.get_current_member(request)
        member_id = member.id
        try:
            result = self.logic.get_user_searches(member_id=member_id)
            serialized_result = GetUserSearchListSerializer(data=result)
            if serialized_result.is_valid():

                return Response(serialized_result.data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):

        data = request.data

        serializer = ServeUserSearchListSerializer(data=data)
        member = self.get_current_member(request)
        member_id = member.id

        if serializer.is_valid():
            query = serializer.data.get(UserSearchVO.QUERY)
            self.logic.save_user_search(member_id=member_id, search_word=query)

            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
