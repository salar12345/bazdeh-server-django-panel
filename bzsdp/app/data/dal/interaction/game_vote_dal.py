from typing import Optional

from bzscl.model.entity.interaction.game_vote_entity import GameVoteEntity
from django.db.models import QuerySet
from ncl.utils.common.singleton import Singleton

from bzsdp.app.data.dao.interaction.game.game_vote_dao import GameVoteDao


class GameVoteDal(metaclass=Singleton):
    def __init__(self):
        self.dao = GameVoteDao()

    def filter(self, *, qs: Optional[QuerySet] = None, **filters) -> QuerySet:
        return self.dao.filter(qs=qs, **filters)

    def get(self, *, qs: Optional[QuerySet] = None, **filters) -> GameVoteEntity:
        return self.dao.get(qs=qs, **filters)

    def exclude(self, *, qs: Optional[QuerySet] = None, **filters) -> QuerySet:
        return self.dao.exclude(qs=qs, **filters)

    def exists(self, qs: Optional[QuerySet] = None, /) -> bool:
        return self.dao.exists(qs)

    def distinct(self, *fields: str, qs: Optional[QuerySet] = None) -> QuerySet:
        return self.dao.distinct(*fields, qs=qs)

    def values(self, *fields: str, qs: Optional[QuerySet] = None) -> QuerySet:
        return self.dao.values(*fields, qs=qs)

    def last(self, qs: QuerySet, /) -> GameVoteEntity:
        return self.dao.last(qs)

    def order_by(self, *fields: str, qs: Optional[QuerySet] = None) -> QuerySet:
        return self.dao.order_by(*fields, qs=qs)
