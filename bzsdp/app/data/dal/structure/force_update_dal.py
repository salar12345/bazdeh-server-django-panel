from typing import Optional

from bzscl.model.entity.structure.force_update_entity import ForceUpdateEntity
from django.db.models import QuerySet, Q
from ncl.utils.common.singleton import Singleton

from bzsdp.app.data.dao.structure.force_update_dao import ForceUpdateDao


class ForceUpdateDal(metaclass=Singleton):
    def __init__(self):
        self.dao = ForceUpdateDao()

    def get(self, *, qs: Optional[QuerySet[ForceUpdateEntity]] = None, **filters) -> ForceUpdateEntity:
        return self.dao.get(qs=qs, **filters)

    def exists(self, *, qs: Optional[QuerySet[ForceUpdateEntity]], **filters) -> bool:
        return self.dao.exists(qs=qs, **filters)

    def get_q_object(self, **filters) -> Q:
        return self.dao.get_q_object(**filters)

    def filter(
            self,
            q_object: Optional[Q] = None,
            qs: Optional[QuerySet[ForceUpdateEntity]] = None,
            **filters
    ) -> QuerySet[ForceUpdateEntity]:
        return self.dao.filter(q_object, qs=qs, **filters)
