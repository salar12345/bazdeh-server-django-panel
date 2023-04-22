from typing import Optional

from django.db.models import QuerySet
from ncl.utils.common.singleton import Singleton
from ncl.dal.dao.entity_base_dao import BaseDao
from bzscl.model.entity.interaction.vote_choices_entity import VoteChoicesEntity


class VoteChoicesDao(BaseDao, metaclass=Singleton):
    model_class = VoteChoicesEntity

    def create(self, **fields) -> VoteChoicesEntity:
        return self.model_class.objects.create(**fields)

    def get(self, *, qs: Optional[QuerySet[VoteChoicesEntity]] = None, **filters) -> VoteChoicesEntity:
        if qs is None:
            return self.model_class.objects.get(**filters)
        return qs.get(**filters)

