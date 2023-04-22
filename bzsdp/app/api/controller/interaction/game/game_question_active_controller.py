from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from ncl.utils.common.singleton import Singleton

from bzsdp.app.api.controller.interaction.game.base_game_question_controller import BaseGameQuestionController
from bzsdp.app.logic.interaction.game_question_logic import GameQuestionLogic
from bzsdp.app.logic.member.member_logic import MemberLogic


class GameQuestionActiveController(BaseGameQuestionController, APIView, metaclass=Singleton):
    def __init__(self, *args, **kwargs):
        BaseGameQuestionController.__init__(self, *args, **kwargs)
        APIView.__init__(self, *args, **kwargs)
        self.game_question_logic = GameQuestionLogic()
        self.member_logic = MemberLogic()

    def get(self, request: Request) -> Response:
        try:
            if self.member_logic.check_if_user_is_logged_in(self.get_current_member(request)):
                questions = self.game_question_logic.get_all_active_questions()
                data = self.enrich_list_question_data(questions, self.get_current_member(request))
                return Response(data, HTTP_200_OK)
            raise Exception('User is not logged in.')
        except Exception:
            return Response(None, HTTP_400_BAD_REQUEST)
