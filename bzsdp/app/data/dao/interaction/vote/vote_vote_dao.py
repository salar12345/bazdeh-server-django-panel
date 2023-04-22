from typing import Optional

from django.db.models import QuerySet
from ncl.utils.common.singleton import Singleton
from ncl.dal.dao.entity_base_dao import BaseDao
from bzscl.model.entity.interaction.vote_vote_entity import VoteVoteEntity


class VoteVoteDao(BaseDao, metaclass=Singleton):
    model_class = VoteVoteEntity

    def create(self, **fields) -> VoteVoteEntity:
        return self.model_class.objects.create(**fields)

    def filter(self, *, qs: Optional[QuerySet[VoteVoteEntity]] = None, **filters) -> QuerySet[VoteVoteEntity]:
        if qs is None:
            return self.model_class.objects.filter(**filters)
        return qs.filter(**filters)

    @staticmethod
    def exists(qs: QuerySet[VoteVoteEntity], /) -> bool:
        return qs.exists()
