from typing import Dict, List, Iterable

from bzscl.model.entity.member.member_entity import MemberEntity
from bzscl.model.entity.interaction.game_question_entity import GameQuestionEntity

from bzsdp.app.api.controller.base_api_view import BasePanelController
from bzsdp.app.api.serializer.interaction.game.game_question_serializer import GameQuestionSerializer
from bzsdp.app.logic.interaction.game_vote_logic import GameVoteLogic



class BaseGameQuestionController(BasePanelController):
    def __init__(self):
        self.game_vote_logic = GameVoteLogic()

    def enrich_list_question_data(self, questions: Iterable, member: MemberEntity) -> List:
        result = list()
        for obj in enumerate(questions):
            result.append(
                GameQuestionSerializer(obj[1]).data
            )
            if current_member_choice := self.game_vote_logic.get_choice_by_member_question_combination(obj[1], member):
                result[obj[0]]['current_member_choice_number'] = current_member_choice.choice_number
        return result

    def enrich_single_question_data(self, question: GameQuestionEntity, member: MemberEntity) -> Dict:
        data = GameQuestionSerializer(question).data
        if current_member_choice := self.game_vote_logic.get_choice_by_member_question_combination(question, member):
            data['current_member_choice_number'] = current_member_choice.choice_number
        return data
