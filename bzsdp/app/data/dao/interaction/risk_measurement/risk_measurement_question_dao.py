from typing import Optional

from bzscl.model.entity.interaction.risk_measurement_question_entity import RiskMeasurementQuestionEntity
from django.db.models import QuerySet
from ncl.utils.common.singleton import Singleton
from ncl.dal.dao.entity_base_dao import BaseDao


class RiskMeasurementQuestionDao(BaseDao, metaclass=Singleton):
    model_class = RiskMeasurementQuestionEntity

    def all(
        self,
        qs: Optional[QuerySet[RiskMeasurementQuestionEntity]] = None,
        /
    ) -> QuerySet[RiskMeasurementQuestionEntity]:
        if qs is not None:
            return qs.all()
        return self.model_class.objects.all()

    @staticmethod
    def order_by(qs: QuerySet[RiskMeasurementQuestionEntity], /, *fields) -> QuerySet[RiskMeasurementQuestionEntity]:
        return qs.order_by(*fields)
