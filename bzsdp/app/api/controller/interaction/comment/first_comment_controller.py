from typing import Dict

from ncl.utils.common.singleton import Singleton
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from bzsdp.app.api.controller.base_api_view import BasePanelController
from bzsdp.app.api.serializer.interaction.comment.comment_serializer import CommentSerializer
from bzsdp.app.logic.interaction.comment_logic import CommentLogic


class FirstCommentController(BasePanelController, APIView, metaclass=Singleton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.comment_logic = CommentLogic()

    def _enrich_comment_data(self, data: Dict) -> Dict:
        data['upvote_count'] = 0
        data['state'] = None
        return data

    def get(self, request: Request) -> Response:
        try:
            return Response(
                not self.comment_logic.check_if_user_has_commented_before(
                    self.get_current_member(request)
                ),
                HTTP_200_OK
            )
        except Exception:
            return Response(None, HTTP_400_BAD_REQUEST)

    def post(self, request: Request) -> Response:
        try:
            comment = self.comment_logic.insert_cached_comment_to_db(
                self.get_current_member(request),
                request.headers['Authorization']
            )
            data = CommentSerializer(comment).data
            return Response(self._enrich_comment_data(data), HTTP_201_CREATED)
        except Exception:
            return Response(None, HTTP_400_BAD_REQUEST)
