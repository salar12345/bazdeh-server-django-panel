from typing import Optional
from django.db.models import QuerySet

from bzscl.model.entity.interaction.game_vote_entity import GameVoteEntity
from ncl.dal.dao.entity_base_dao import BaseDao
from ncl.utils.common.singleton import Singleton


class GameVoteDao(BaseDao, metaclass=Singleton):
    model_class = GameVoteEntity

    def exists(self, qs: Optional[QuerySet] = None, /) -> bool:
        if qs is None:
            return self.model_class.objects.exists()
        return qs.exists()

    def filter(self, *, qs: Optional[QuerySet] = None, **filters) -> QuerySet:
        if qs is None:
            return self.model_class.objects.filter(**filters)
        return qs.filter(**filters)

    def get(self, *, qs: Optional[QuerySet] = None, **filters) -> GameVoteEntity:
        if qs is None:
            return self.model_class.objects.get(**filters)
        return qs.get(**filters)

    def exclude(self, *, qs: Optional[QuerySet] = None, **filters) -> QuerySet:
        if qs is None:
            return self.model_class.objects.filter(**filters)
        return qs.filter(**filters)

    def distinct(self, *fields: str, qs: Optional[QuerySet] = None) -> QuerySet:
        if qs is None:
            return self.model_class.objects.distinct(*fields)
        return qs.distinct(*fields)

    def values(self, *fields: str, qs: Optional[QuerySet] = None) -> QuerySet:
        if qs is None:
            return self.model_class.objects.values(*fields)
        return qs.values(*fields)

    def order_by(self, *fields: str, qs: Optional[QuerySet] = None) -> QuerySet:
        if qs is None:
            return self.model_class.objects.order_by(*fields)
        return qs.order_by(*fields)

    @staticmethod
    def last(qs: QuerySet, /) -> GameVoteEntity:
        return qs.last()
