from typing import Optional

from bzscl.model.entity.interaction.risk_measurement_choice_entity import RiskMeasurementChoiceEntity
from django.db.models import QuerySet
from ncl.utils.common.singleton import Singleton

from bzsdp.app.data.dao.interaction.risk_measurement.risk_measurement_choice_dao import RiskMeasurementChoiceDao


class RiskMeasurementChoiceDal(metaclass=Singleton):
    def __init__(self):
        self.risk_measurement_choice_dao = RiskMeasurementChoiceDao()

    def filter(
            self,
            *,
            qs: Optional[QuerySet[RiskMeasurementChoiceEntity]] = None,
            **filters
    ) -> QuerySet[RiskMeasurementChoiceEntity]:
        return self.risk_measurement_choice_dao.filter(qs=qs, **filters)

    def get(
        self,
        *,
        qs: Optional[QuerySet[RiskMeasurementChoiceEntity]] = None,
        **filters
    ) -> RiskMeasurementChoiceEntity:
        return self.risk_measurement_choice_dao.get(qs=qs, **filters)

    def order_by(self, qs: QuerySet[RiskMeasurementChoiceEntity], /, *fields) -> QuerySet[RiskMeasurementChoiceEntity]:
        return self.risk_measurement_choice_dao.order_by(qs, *fields)

    def exists(self, qs: Optional[QuerySet[RiskMeasurementChoiceEntity]] = None, /) -> bool:
        return self.risk_measurement_choice_dao.exists(qs)
