from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from ncl.utils.common.singleton import Singleton

from bzsdp.app.api.controller.base_api_view import BasePanelController
from bzsdp.app.api.serializer.interaction.game.game_question_serializer import GameQuestionSerializer
from bzsdp.app.logic.interaction.game_question_logic import GameQuestionLogic

from bzsdp.app.logic.member.member_logic import MemberLogic

class GameQuestionNotAttendedActiveController(BasePanelController, APIView, metaclass=Singleton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game_question_logic = GameQuestionLogic()
        self.member_logic = MemberLogic()

    def get(self, request: Request) -> Response:
        try:
            if self.member_logic.check_if_user_is_logged_in(self.get_current_member(request)):
                not_attended_active_questions = self.game_question_logic.get_active_question_without_member_attendance(
                    self.get_current_member(request)
                )
                return Response(
                    GameQuestionSerializer(not_attended_active_questions, many=True).data,
                    HTTP_200_OK
                )
            raise Exception('User is not logged in.')
        except Exception:
            return Response(None, HTTP_400_BAD_REQUEST)
