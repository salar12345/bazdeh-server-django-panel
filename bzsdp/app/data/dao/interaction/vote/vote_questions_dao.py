from typing import Optional

from ncl.utils.common.singleton import Singleton
from ncl.dal.dao.entity_base_dao import BaseDao
from bzscl.model.entity.interaction.vote_questions_entity import VoteQuestionsEntity
from django.db.models import QuerySet


class VoteQuestionsDao(BaseDao, metaclass=Singleton):
    model_class = VoteQuestionsEntity

    @staticmethod
    def exists(qs: QuerySet[VoteQuestionsEntity], /) -> bool:
        return qs.exists()

    def filter(self, *, qs: Optional[QuerySet[VoteQuestionsEntity]] = None, **filters) -> QuerySet:
        if qs is None:
            return self.model_class.objects.filter(**filters)
        return qs.filter(**filters)

    def get(self, *, qs: Optional[QuerySet[VoteQuestionsEntity]] = None, **filters) -> VoteQuestionsEntity:
        if qs is None:
            return self.model_class.objects.get(**filters)
        return qs.get(**filters)

    @staticmethod
    def first(qs: QuerySet[VoteQuestionsEntity], /) -> VoteQuestionsEntity:
        return qs.first()

    @staticmethod
    def save(obj: VoteQuestionsEntity, /) -> None:
        obj.save()
