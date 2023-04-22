from typing import Optional
from django.db.models import QuerySet

from bzscl.model.entity.interaction.game_choices_entity import GameChoicesEntity
from ncl.dal.dao.entity_base_dao import BaseDao
from ncl.utils.common.singleton import Singleton


class GameChoicesDao(BaseDao, metaclass=Singleton):
    model_class = GameChoicesEntity

    def exists(self, qs: Optional[QuerySet] = None, /) -> bool:
        if qs is None:
            return self.model_class.objects.exists()
        return qs.exists()

    def filter(self, *, qs: Optional[QuerySet] = None, **filters) -> QuerySet:
        if qs is None:
            return self.model_class.objects.filter(**filters)
        return qs.filter(**filters)
