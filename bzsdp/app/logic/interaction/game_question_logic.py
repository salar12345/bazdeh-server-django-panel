from typing import List, Union
from uuid import UUID

from bzscl.model.entity.interaction.game_question_entity import GameQuestionEntity
from bzscl.model.entity.member.member_entity import MemberEntity
from django.db.models import QuerySet
from ncl.utils.common.singleton import Singleton

from bzsdp.app.data.dal.interaction.game_question_dal import GameQuestionDal
from bzsdp.app.data.dal.interaction.game_vote_dal import GameVoteDal
from bzsdp.app.model.vo.interaction.game_vo import GameVo


class GameQuestionLogic(metaclass=Singleton):
    def __init__(self):
        self.game_question_dal = GameQuestionDal()
        self.game_vote_dal = GameVoteDal()

    def get_all_active_questions(self) -> QuerySet:
        filters = {GameVo.IS_ACTIVE: True}
        return self.game_question_dal.filter(**filters)

    def get_all_member_attended_inactive_questions(self, member: MemberEntity) -> List:
        filters = {
            f'{GameVo.CHOICE}__{GameVo.QUESTION}__{GameVo.IS_ACTIVE}': False,
            f'{GameVo.MEMBER}': member
        }
        votes = self.game_vote_dal.filter(**filters)
        return [vote.choice.question for vote in votes]

    def get_questions_by_activity_status(self, status: bool) -> QuerySet:
        filters = {GameVo.IS_ACTIVE: status}
        return self.game_question_dal.filter(**filters)

    def get_active_question_without_member_attendance(self, member: MemberEntity) -> QuerySet:
        active_questions = self.get_all_active_questions()

        member_votes_filters = {GameVo.MEMBER: member}
        member_attended_questions_id_set = self.game_vote_dal.values(
            f'{GameVo.CHOICE}__{GameVo.QUESTION}',
            qs=self.game_vote_dal.distinct(
                f'{GameVo.CHOICE}__{GameVo.QUESTION}',
                qs=self.game_vote_dal.filter(**member_votes_filters)
            )
        )

        exclude_attended_questions_filters = {f'{GameVo.ID}__in': member_attended_questions_id_set}
        return self.game_question_dal.exclude(qs=active_questions, **exclude_attended_questions_filters)

    def get_priceables_of_active_questions(self) -> List:
        active_questions = self.get_all_active_questions()
        priceables_queryset = self.game_question_dal.values(
            GameVo.PRICEABLE,
            qs=self.game_question_dal.distinct(GameVo.PRICEABLE, qs=active_questions)
        )
        return [obj[GameVo.PRICEABLE] for obj in priceables_queryset]

    def get_question_by_id(self, id_: Union[UUID, str]) -> GameQuestionEntity:
        filters = {GameVo.ID: id_}
        return self.game_question_dal.get(**filters)
