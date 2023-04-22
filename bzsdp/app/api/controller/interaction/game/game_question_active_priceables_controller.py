from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from ncl.utils.common.singleton import Singleton

from bzsdp.app.api.controller.base_api_view import BasePanelController
from bzsdp.app.logic.interaction.game_question_logic import GameQuestionLogic


class GameQuestionActivePriceablesController(BasePanelController, APIView, metaclass=Singleton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game_question_logic = GameQuestionLogic()

    def get(self, request: Request) -> Response:
        try:
            return Response(
                self.game_question_logic.get_priceables_of_active_questions(),
                HTTP_200_OK
            )
        except Exception:
            return Response(None, HTTP_400_BAD_REQUEST)
