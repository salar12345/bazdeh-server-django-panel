from typing import List, Optional

from bzscl.model.entity.interaction.vote_choices_entity import VoteChoicesEntity
from bzscl.model.entity.interaction.vote_questions_entity import VoteQuestionsEntity
from bzscl.model.entity.member.member_entity import MemberEntity
from bzscl.model.vo.interaction.vote_choices_vo import VoteChoicesVo
from bzscl.model.vo.interaction.vote_questions_vo import VoteQuestionsVo
from bzscl.model.vo.interaction.vote_vote_vo import VoteVoteVo
from django.utils import timezone
from ncl.utils.common.singleton import Singleton

from bzsdp.app.data.dal.interaction.vote_questions_dal import VoteQuestionsDal
from bzsdp.app.data.dal.interaction.vote_choices_dal import VoteChoicesDal
from bzsdp.app.data.dal.interaction.vote_vote_dal import VoteVoteDal
from bzsdp.app.data.dal.interaction.vote_dismiss_dal import VoteDismissDal


class VoteLogic(metaclass=Singleton):
    def __init__(self):
        self.vote_questions_dal = VoteQuestionsDal()
        self.vote_choices_dal = VoteChoicesDal()
        self.vote_vote_dal = VoteVoteDal()
        self.vote_dismiss_dal = VoteDismissDal()

    def active_question_exists(self, member: MemberEntity, app_version: str) -> bool:
        active_question_filter = {
            f'{VoteQuestionsVo.EXPIRATION_TIME}__gt': timezone.now(),
            VoteQuestionsVo.APP_VERSION: app_version,
            VoteQuestionsVo.IS_ACTIVE: True
        }
        queryset = self.vote_questions_dal.filter(**active_question_filter)
        if not self.vote_questions_dal.exists(queryset):
            return False
        question = self.vote_questions_dal.first(queryset)
        if self._check_member_action_existance(member, question):
            return False
        return True

    def get_active_question(self, member: MemberEntity) -> VoteQuestionsEntity:
        active_question_filter = {
            f'{VoteQuestionsVo.EXPIRATION_TIME}__gt': timezone.now(),
            VoteQuestionsVo.IS_ACTIVE: True
        }
        question = self.vote_questions_dal.get(**active_question_filter)
        if not self._check_member_action_existance(member, question):
            return question
        raise Exception('There isn\'t an active question for this member.')

    def submit_member_action(
            self,
            member: MemberEntity,
            question_id: str,
            choice_ids: Optional[List[str]] = None
    ) -> None:
        question = self._get_active_question_by_id(question_id)
        if self._check_member_action_existance(member, question):
            raise Exception('Member already submitted action for this question.')
        if choice_ids is not None:
            if len(choice_ids) > 1 and not question.multiple_choices:
                raise Exception('Can\'t submit multiple votes for question.')
            for choice_id in choice_ids:
                choice = self._get_choice_by_question_and_id(question, choice_id)
                self.vote_vote_dal.create(member=member, choice=choice)
        else:
            self.vote_dismiss_dal.add(member, question)

    def _get_choice_by_question_and_id(self, question: VoteQuestionsEntity, choice_id: str) -> VoteChoicesEntity:
        choice_filter = {
            VoteChoicesVo.QUESTION: question,
            VoteChoicesVo.ID: choice_id
        }
        return self.vote_choices_dal.get(**choice_filter)

    def _get_active_question_by_id(self, question_id: str) -> VoteQuestionsEntity:
        question_filter = {
            VoteQuestionsVo.ID: question_id,
            VoteQuestionsVo.IS_ACTIVE: True,
            f'{VoteQuestionsVo.EXPIRATION_TIME}__gt': timezone.now()
        }
        return self.vote_questions_dal.get(**question_filter)

    def _check_member_action_existance(self, member: MemberEntity, question: VoteQuestionsEntity) -> bool:
        return (
            self._check_member_vote_existance(member, question) or
            self._check_member_dismiss_existance(member, question)
        )

    def _check_member_vote_existance(self, member: MemberEntity, question: VoteQuestionsEntity) -> bool:
        vote_filter = {
            VoteVoteVo.MEMBER: member,
            f'{VoteVoteVo.CHOICE}__{VoteChoicesVo.QUESTION}': question
        }
        return self.vote_vote_dal.exists(
            self.vote_vote_dal.filter(**vote_filter)
        )

    def _check_member_dismiss_existance(self, member: MemberEntity, question: VoteQuestionsEntity) -> bool:
        if dismissals := self.vote_dismiss_dal.get(question):
            if str(member.id) in dismissals:
                return True
        return False
