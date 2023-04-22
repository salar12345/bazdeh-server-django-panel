from typing import Optional

from bzscl.model.entity.structure.force_update_entity import ForceUpdateEntity
from django.db.models import QuerySet, Q
from ncl.utils.common.singleton import Singleton
from ncl.dal.dao.entity_base_dao import BaseDao


class ForceUpdateDao(BaseDao, metaclass=Singleton):
    model_class = ForceUpdateEntity

    def get(self, *, qs: Optional[QuerySet[ForceUpdateEntity]] = None, **filters) -> ForceUpdateEntity:
        if qs is None:
            return self.model_class.objects.get(**filters)
        return qs.get(**filters)

    def exists(self, *, qs: Optional[QuerySet[ForceUpdateEntity]], **filters) -> bool:
        if qs is None:
            return self.model_class.objects.filter(**filters).exists()
        return qs.exists()

    @staticmethod
    def get_q_object(**filters) -> Q:
        return Q(**filters)

    def filter(
            self,
            q_object: Optional[Q] = None,
            qs: Optional[QuerySet[ForceUpdateEntity]] = None,
            **filters
    ) -> QuerySet[ForceUpdateEntity]:
        if qs is None:
            return self.model_class.objects.filter(q_object, **filters)
        return qs.filter(q_object, **filters)
