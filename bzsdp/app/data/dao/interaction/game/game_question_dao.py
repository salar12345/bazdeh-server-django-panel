from typing import Optional
from django.db.models import QuerySet

from bzscl.model.entity.interaction.game_question_entity import GameQuestionEntity
from ncl.dal.dao.entity_base_dao import BaseDao
from ncl.utils.common.singleton import Singleton


class GameQuestionDao(BaseDao, metaclass=Singleton):
    model_class = GameQuestionEntity

    def filter(self, *, qs: Optional[QuerySet] = None, **filters: str) -> QuerySet:
        if qs is None:
            return self.model_class.objects.filter(**filters)
        return qs.filter(**filters)

    def exclude(self, *, qs: Optional[QuerySet] = None, **filters) -> QuerySet:
        if qs is None:
            return self.model_class.objects.exclude(**filters)
        return qs.exclude(**filters)

    def get(self, *, qs: Optional[QuerySet] = None, **filters: str) -> GameQuestionEntity:
        if qs is None:
            return self.model_class.objects.get(**filters)
        return qs.get(**filters)

    def distinct(self, *fields: str, qs: Optional[QuerySet] = None) -> QuerySet:
        if qs is None:
            return self.model_class.objects.distinct(*fields)
        return qs.distinct(*fields)

    def values(self, *fields: str, qs: Optional[QuerySet] = None) -> QuerySet:
        if qs is None:
            return self.model_class.objects.values(*fields)
        return qs.values(*fields)
