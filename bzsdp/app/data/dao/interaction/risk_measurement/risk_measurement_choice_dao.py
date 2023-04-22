from typing import Optional

from bzscl.model.entity.interaction.risk_measurement_choice_entity import RiskMeasurementChoiceEntity
from django.db.models import QuerySet
from ncl.utils.common.singleton import Singleton
from ncl.dal.dao.entity_base_dao import BaseDao


class RiskMeasurementChoiceDao(BaseDao, metaclass=Singleton):
    model_class = RiskMeasurementChoiceEntity

    def filter(
        self,
        *,
        qs: Optional[QuerySet[RiskMeasurementChoiceEntity]] = None,
        **filters
    ) -> QuerySet[RiskMeasurementChoiceEntity]:
        if qs is not None:
            return qs.filter(**filters)
        return self.model_class.objects.filter(**filters)

    def get(
        self,
        *,
        qs: Optional[QuerySet[RiskMeasurementChoiceEntity]] = None,
        **filters
    ) -> RiskMeasurementChoiceEntity:
        if qs is not None:
            return qs.get(**filters)
        return self.model_class.objects.get(**filters)

    @staticmethod
    def order_by(qs: QuerySet[RiskMeasurementChoiceEntity], /, *fields) -> QuerySet[RiskMeasurementChoiceEntity]:
        return qs.order_by(*fields)

    def exists(self, qs: Optional[QuerySet[RiskMeasurementChoiceEntity]] = None, /) -> bool:
        if qs is not None:
            return qs.exists()
        return self.model_class.objects.exists()
