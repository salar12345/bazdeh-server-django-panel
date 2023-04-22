from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from ncl.utils.common.singleton import Singleton

from bzsdp.app.logic.interaction.vote.vote_logic import VoteLogic
from bzsdp.app.api.serializer.interaction.vote.vote_questions_serializer import VoteQuestionsSerializer
from bzsdp.app.api.controller.base_api_view import BasePanelController


class VoteController(APIView, BasePanelController, metaclass=Singleton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.vote_logic = VoteLogic()

    def get(self, request: Request) -> Response:
        try:
            return Response(
                VoteQuestionsSerializer(
                    self.vote_logic.get_active_question(
                        self.get_current_member(request)
                    )
                ).data,
                HTTP_200_OK
            )
        except Exception:
            return Response(None, HTTP_400_BAD_REQUEST)

    def post(self, request: Request) -> Response:
        try:
            input_date = [self.get_current_member(request), request.data['question_id']]
            if choice_ids := request.data.get('choice_ids'):
                input_date.append(choice_ids)
            self.vote_logic.submit_member_action(*input_date)
            return Response(None, HTTP_200_OK)
        except Exception:
            return Response(None, HTTP_400_BAD_REQUEST)
