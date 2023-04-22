from typing import Any, Optional

from bzscl.model.entity.interaction.risk_measurement_vote_entity import RiskMeasurementVoteEntity
from django.db.models import QuerySet
from ncl.utils.common.singleton import Singleton
from ncl.dal.dao.entity_base_dao import BaseDao


class RiskMeasurementVoteDao(BaseDao, metaclass=Singleton):
    model_class = RiskMeasurementVoteEntity

    def filter(
        self,
        *,
        qs: Optional[QuerySet[RiskMeasurementVoteEntity]] = None,
        **filters
    ) -> QuerySet[RiskMeasurementVoteEntity]:
        if qs is not None:
            return qs.filter(**filters)
        return self.model_class.objects.filter(**filters)

    def create(self, **fields) -> RiskMeasurementVoteEntity:
        return self.model_class.objects.create(**fields)

    def exists(self, qs: Optional[QuerySet[RiskMeasurementVoteEntity]] = None, /) -> bool:
        if qs is not None:
            return qs.exists()
        return self.model_class.objects.exists()

    @staticmethod
    def delete(
        *,
        qs: Optional[QuerySet[RiskMeasurementVoteEntity]] = None,
        obj: Optional[RiskMeasurementVoteEntity] = None,
        hard_delete: Optional[bool] = False
    ) -> None:
        if qs is not None:
            qs.delete()
        if obj is not None:
            obj.delete(hard_delete=hard_delete)

    def values_list(
        self,
        *fields,
        qs: Optional[QuerySet[RiskMeasurementVoteEntity]] = None,
        flat: Optional[bool] = False,
        named: Optional[bool] = False
    ) -> QuerySet[Any]:
        if qs is not None:
            return qs.values_list(*fields, flat=flat, named=named)
        return self.model_class.objects.values_list(*fields, flat=flat, named=named)
