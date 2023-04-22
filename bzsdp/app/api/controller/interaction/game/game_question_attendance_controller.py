from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from ncl.utils.common.singleton import Singleton

from bzsdp.app.api.controller.base_api_view import BasePanelController
from bzsdp.app.logic.interaction.game_question_logic import GameQuestionLogic
from bzsdp.app.logic.interaction.game_vote_logic import GameVoteLogic

from bzsdp.app.logic.member.member_logic import MemberLogic

class GameQuestionAttendanceController(BasePanelController, APIView, metaclass=Singleton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.member_logic = MemberLogic()
        self.game_vote_logic = GameVoteLogic()
        self.game_question_logic = GameQuestionLogic()

    def post(self, request: Request) -> Response:
        try:
            question = self.game_question_logic.get_question_by_id(request.data['question_id'])
            member = self.get_current_member(request)
            return Response(
                self.game_vote_logic.check_for_member_question_attendance(member, question),
                HTTP_200_OK
            )
        except Exception:
            return Response(None, HTTP_400_BAD_REQUEST)
