from datetime import datetime
from typing import Union

from bzscl.model.entity.member.member_entity import MemberEntity
from bzscl.model.entity.interaction.game_choices_entity import GameChoicesEntity
from bzscl.model.entity.interaction.game_question_entity import GameQuestionEntity
from bzscl.model.entity.interaction.game_vote_entity import GameVoteEntity
from django.db.models import QuerySet
from ncl.utils.common.singleton import Singleton

from bzsdp.app.data.dal.interaction.game_vote_dal import GameVoteDal
from bzsdp.app.data.dal.interaction.game_choices_dal import GameChoicesDal
from bzsdp.app.model.vo.interaction.game_vo import GameVo


class GameVoteLogic(metaclass=Singleton):
    def __init__(self):
        self.game_vote_dal = GameVoteDal()
        self.game_choice_dal = GameChoicesDal()

    def check_for_member_choice_combination_existance(self, member: MemberEntity, choice: GameChoicesEntity) -> bool:
        filters = {GameVo.MEMBER: member, GameVo.CHOICE: choice}
        return self.game_vote_dal.exists(
            self.game_vote_dal.filter(
                **filters
            )
        )

    def check_for_member_question_attendance(self, member: MemberEntity, question: GameQuestionEntity) -> bool:
        filters = {GameVo.MEMBER: member, f'{GameVo.CHOICE}__{GameVo.QUESTION}': question}
        return self.game_vote_dal.exists(
            self.game_vote_dal.filter(**filters)
        )

    def mark_all_member_unseen_votes_as_seen(self, member: MemberEntity) -> None:
        filters = {GameVo.MEMBER: member, GameVo.MEMBER_RESULT_SEEN: False}
        votes = self.game_vote_dal.filter(**filters)
        for vote in votes:
            vote.member_result_seen = True
            vote.save()

    @staticmethod
    def _mark_vote_as_seen_result(vote: GameVoteEntity) -> None:
        vote.member_result_seen = True
        vote.save()

    def check_if_member_has_unseen_vote(self, member: MemberEntity) -> bool:
        return self.get_member_last_unseen_attended_question_result(member) is not None

    def get_member_last_unseen_attended_question_result(self, member: MemberEntity) -> Union[GameQuestionEntity, None]:
        votes = self._get_member_all_unseen_votes(member)
        for vote in votes:
            if self._check_if_question_has_correct_choice(vote.choice.question):
                return vote.choice.question

    def _get_member_all_unseen_votes(self, member: MemberEntity) -> QuerySet:
        filters = {
            GameVo.MEMBER: member,
            GameVo.MEMBER_RESULT_SEEN: False,
            f'{GameVo.CHOICE}__{GameVo.QUESTION}__{GameVo.PREDICTION_RESULT_DATE}'
            '__lt': datetime.now()
        }
        return self.game_vote_dal.order_by(
            f'-{GameVo.CHOICE}__{GameVo.QUESTION}__{GameVo.PREDICTION_RESULT_DATE}',
            qs=self.game_vote_dal.filter(**filters)
        )

    def _check_if_question_has_correct_choice(self, question: GameQuestionEntity) -> bool:
        filters = {GameVo.QUESTION: question, GameVo.IS_CORRECT: True}
        return self.game_choice_dal.exists(
            self.game_choice_dal.filter(**filters)
        )

    def get_choice_by_member_question_combination(
        self,
        question: GameQuestionEntity,
        member: MemberEntity
    ) -> Union[GameChoicesEntity, None]:
        try:
            filters = {GameVo.MEMBER: member, f'{GameVo.CHOICE}__{GameVo.QUESTION}': question}
            return self.game_vote_dal.get(**filters).choice
        except GameVoteEntity.DoesNotExist:
            return None
