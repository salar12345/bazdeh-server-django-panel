from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from ncl.utils.common.singleton import Singleton

from bzsdp.app.api.controller.interaction.game.base_game_question_controller import BaseGameQuestionController


class GameQuestionLastAttendanceResultController(BaseGameQuestionController, APIView, metaclass=Singleton):
    def __init__(self, *args, **kwargs):
        BaseGameQuestionController.__init__(self, *args, **kwargs)
        APIView.__init__(self, *args, **kwargs)

    def get(self, request: Request) -> Response:
        try:
            question = self.game_vote_logic.get_member_last_unseen_attended_question_result(
                self.get_current_member(request)
            )
            if question:
                member = self.get_current_member(request)
                self.game_vote_logic.mark_all_member_unseen_votes_as_seen(member)
                return Response(
                    self.enrich_single_question_data(question, member),
                    HTTP_200_OK
                )
            else:
                raise Exception('There is no unseen results for this member.')
        except Exception:
            return Response(None, HTTP_400_BAD_REQUEST)
