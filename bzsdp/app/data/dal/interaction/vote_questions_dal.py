from typing import Optional

from bzscl.model.entity.interaction.vote_questions_entity import VoteQuestionsEntity
from django.db.models import QuerySet
from ncl.utils.common.singleton import Singleton

from bzsdp.app.data.dao.interaction.vote.vote_questions_dao import VoteQuestionsDao


class VoteQuestionsDal(metaclass=Singleton):
    def __init__(self):
        self.dao = VoteQuestionsDao()

    def filter(self, *, qs: Optional[QuerySet[VoteQuestionsEntity]] = None, **filters) -> QuerySet:
        return self.dao.filter(qs=qs, **filters)

    def get(self, *, qs: Optional[QuerySet[VoteQuestionsEntity]] = None, **filters) -> VoteQuestionsEntity:
        return self.dao.get(qs=qs, **filters)

    def exists(self, qs: QuerySet[VoteQuestionsEntity], /) -> bool:
        return self.dao.exists(qs)

    def first(self, qs: QuerySet[VoteQuestionsEntity], /) -> VoteQuestionsEntity:
        return self.dao.first(qs)

    def save(self, obj: VoteQuestionsEntity, /) -> None:
        self.dao.save(obj)
