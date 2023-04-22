from typing import Optional

from bzscl.model.entity.interaction.risk_measurement_question_entity import RiskMeasurementQuestionEntity
from django.db.models import QuerySet
from ncl.utils.common.singleton import Singleton
from ncl.utils.common.lru_ttl_cache import lru_ttl_cache

from bzsdp.app.data.dao.interaction.risk_measurement.risk_measurement_question_dao import RiskMeasurementQuestionDao


class RiskMeasurementQuestionDal(metaclass=Singleton):
    def __init__(self):
        self.risk_measurement_dao = RiskMeasurementQuestionDao()

    @lru_ttl_cache(ttl_seconds=60 * 60)
    def all(
            self,
            qs: Optional[QuerySet[RiskMeasurementQuestionEntity]] = None,
            /
    ) -> QuerySet[RiskMeasurementQuestionEntity]:
        return self.risk_measurement_dao.all(qs)

    def order_by(
        self,
        qs: QuerySet[RiskMeasurementQuestionEntity],
        /,
        *fields
    ) -> QuerySet[RiskMeasurementQuestionEntity]:
        return self.risk_measurement_dao.order_by(qs, *fields)
