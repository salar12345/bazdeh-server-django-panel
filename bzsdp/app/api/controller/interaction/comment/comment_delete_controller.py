from ncl.utils.common.singleton import Singleton
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from bzsdp.app.api.controller.base_api_view import BasePanelController
from bzsdp.app.logic.interaction.comment_logic import CommentLogic


class CommentDeleteController(APIView, BasePanelController, metaclass=Singleton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.comment_logic = CommentLogic()

    def post(self, request: Request) -> Response:
        try:
            self.comment_logic.delete_comment(
                self.get_current_member(request),
                request.data['comment_id']
            )
            return Response(None, HTTP_204_NO_CONTENT)
        except Exception:
            return Response(None, HTTP_400_BAD_REQUEST)
