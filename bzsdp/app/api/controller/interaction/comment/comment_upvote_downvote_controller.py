from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ncl.utils.common.singleton import Singleton
from bzsdp.app.api.controller.base_api_view import BasePanelController
from bzsdp.app.api.serializer.interaction.comment.comment_upvote_downvote_Serializer import \
    CommentUpvoteDownvoteSerializer

from bzscl.model.vo.interaction.comment_vo import CommentVo

from bzsdp.app.logic.interaction.comment_logic import CommentLogic


class CommentUpvoteDownvoteController(BasePanelController, APIView, metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.logic = CommentLogic()

    def post(self, request):

        data = request.data
        serializer = CommentUpvoteDownvoteSerializer(data=data)
        if serializer.is_valid():
            member = self.get_current_member(request)
            comment_id = serializer.data.get(CommentVo.COMMENT_ID)
            upvote_or_downvote = serializer.data.get(CommentVo.UPVOTE_OR_DOWNVOTE)
            try:
                response = self.logic.do_upvote_or_downvote(member=member,
                                                            comment_id=comment_id,
                                                            upvote_or_downvote=upvote_or_downvote)

                return Response(response, status=status.HTTP_201_CREATED)
            except Exception:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
