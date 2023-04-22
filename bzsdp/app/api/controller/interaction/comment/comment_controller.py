from typing import Dict

from ncl.utils.common.singleton import Singleton
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from bzsdp.app.api.controller.base_api_view import BasePanelController
from bzsdp.app.logic.interaction.comment_logic import CommentLogic

from bzsdp.app.logic.member.member_logic import MemberLogic
from bzsdp.app.api.serializer.interaction.comment.comment_serializer import CommentSerializer


class CommentController(BasePanelController, APIView, metaclass=Singleton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.comment_logic = CommentLogic()
        self.member_logic = MemberLogic()

    def _enrich_comment_data(self, data: Dict) -> Dict:
        data['upvote_count'] = 0
        data['state'] = None
        return data

    def post(self, request: Request) -> Response:
        try:
            data = request.data.copy()
            data['member'] = self.get_current_member(request)
            if data.get('reply_to'):
                data['reply_to'] = self.comment_logic.get_comment(data['reply_to'])
            if data.get('mentioned_member'):
                data['mentioned_member'] = self.member_logic.get_member_by_id(data['mentioned_member'])
            if self.member_logic.check_if_user_is_logged_in(data['member']):
                if data.get('first_comment'):
                    data['jwt_token'] = request.headers['Authorization']
                    self.comment_logic.add_comment(**data)
                    return Response(None, HTTP_200_OK)
                else:
                    data['first_comment'] = False
                    comment = self.comment_logic.add_comment(**data)
                    data = CommentSerializer(comment).data
                    return Response(self._enrich_comment_data(data), HTTP_201_CREATED)
            else:
                raise Exception('User is not logged in.')
        except Exception:
            return Response(None, HTTP_400_BAD_REQUEST)
