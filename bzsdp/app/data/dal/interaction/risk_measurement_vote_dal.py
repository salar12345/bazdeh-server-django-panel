from typing import Any, Optional

from bzscl.model.entity.interaction.risk_measurement_vote_entity import RiskMeasurementVoteEntity
from django.db.models import QuerySet
from ncl.utils.common.singleton import Singleton

from bzsdp.app.data.dao.interaction.risk_measurement.risk_measurement_vote_dao import RiskMeasurementVoteDao


class RiskMeasurementVoteDal(metaclass=Singleton):
    def __init__(self):
        self.risk_measurement_vote_dao = RiskMeasurementVoteDao()

    def filter(
            self,
            *,
            qs: Optional[QuerySet[RiskMeasurementVoteEntity]] = None,
            **filters
    ) -> QuerySet[RiskMeasurementVoteEntity]:
        return self.risk_measurement_vote_dao.filter(qs=qs, **filters)

    def create(self, **fields) -> RiskMeasurementVoteEntity:
        return self.risk_measurement_vote_dao.create(**fields)

    def exists(self, qs: Optional[QuerySet[RiskMeasurementVoteEntity]] = None, /) -> bool:
        return self.risk_measurement_vote_dao.exists(qs)

    def delete(
        self,
        *,
        qs: Optional[QuerySet[RiskMeasurementVoteEntity]] = None,
        obj: Optional[RiskMeasurementVoteEntity] = None,
        hard_delete: Optional[bool] = False
    ) -> None:
        return self.risk_measurement_vote_dao.delete(qs=qs, obj=obj, hard_delete=hard_delete)

    def values_list(
            self,
            *fields,
            qs: Optional[QuerySet[RiskMeasurementVoteEntity]] = None,
            flat: Optional[bool] = False,
            named: Optional[bool] = False
    ) -> QuerySet[Any]:
        return self.risk_measurement_vote_dao.values_list(*fields, qs=qs, flat=flat, named=named)
