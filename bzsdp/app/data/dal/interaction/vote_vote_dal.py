from typing import Optional

from bzscl.model.entity.interaction.vote_vote_entity import VoteVoteEntity
from django.db.models import QuerySet
from ncl.utils.common.singleton import Singleton

from bzsdp.app.data.dao.interaction.vote.vote_vote_dao import VoteVoteDao


class VoteVoteDal(metaclass=Singleton):
    def __init__(self):
        self.dao = VoteVoteDao()

    def create(self, **fields) -> VoteVoteEntity:
        return self.dao.create(**fields)

    def filter(self, *, qs: Optional[QuerySet[VoteVoteEntity]] = None, **filters) -> QuerySet[VoteVoteEntity]:
        return self.dao.filter(qs=qs, **filters)

    def exists(self, qs: QuerySet[VoteVoteEntity], /) -> bool:
        return self.dao.exists(qs)
