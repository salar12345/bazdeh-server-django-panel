from typing import Dict, List

from bzscl.model.entity.interaction.risk_measurement_question_entity import RiskMeasurementQuestionEntity
from bzscl.model.entity.member.member_entity import MemberEntity
from bzscl.model.vo.interaction.risk_measurement_question_vo import RiskMeasurementQuestionVo
from bzscl.model.vo.interaction.risk_measurement_choice_vo import RiskMeasurementChoiceVo
from bzscl.model.vo.interaction.risk_measurement_vote_vo import RiskMeasurementVoteVo
from django.db.models import QuerySet
from ncl.utils.common.singleton import Singleton

from bzsdp.app.data.dal.interaction.risk_measurement_question_dal import RiskMeasurementQuestionDal
from bzsdp.app.data.dal.interaction.risk_measurement_choice_dal import RiskMeasurementChoiceDal
from bzsdp.app.data.dal.interaction.risk_measurement_vote_dal import RiskMeasurementVoteDal
from bzsdp.app.model.vo.interaction.risk_measurement_vo import RiskMeasurementVo
from bzsdp.app.model.enum.interaction.risk_tolerance_type import RiskToleranceType


class RiskMeasurementLogic(metaclass=Singleton):
    SCORE_RESULT_MAPPER = {
        RiskToleranceType.RISK_AVOIDER: {
            RiskMeasurementVo.STOCK_FOUND_CRYPTOCURRENCY: 0,
            RiskMeasurementVo.GOLD_DOLLAR: 0,
            RiskMeasurementVo.BANK_CACHE_FIXED_INCOME_BONDS: 100
        },
        RiskToleranceType.CATIOUS: {
            RiskMeasurementVo.STOCK_FOUND_CRYPTOCURRENCY: 5,
            RiskMeasurementVo.GOLD_DOLLAR: 25,
            RiskMeasurementVo.BANK_CACHE_FIXED_INCOME_BONDS: 70
        },
        RiskToleranceType.MODERATE: {
            RiskMeasurementVo.STOCK_FOUND_CRYPTOCURRENCY: 20,
            RiskMeasurementVo.GOLD_DOLLAR: 30,
            RiskMeasurementVo.BANK_CACHE_FIXED_INCOME_BONDS: 50
        },
        RiskToleranceType.RISK_TAKER: {
            RiskMeasurementVo.STOCK_FOUND_CRYPTOCURRENCY: 80,
            RiskMeasurementVo.GOLD_DOLLAR: 15,
            RiskMeasurementVo.BANK_CACHE_FIXED_INCOME_BONDS: 5
        }
    }

    def __init__(self):
        self.risk_measurement_question_dal = RiskMeasurementQuestionDal()
        self.risk_measurement_choice_dal = RiskMeasurementChoiceDal()
        self.risk_measurement_vote_dal = RiskMeasurementVoteDal()

    def get_questions(self) -> QuerySet[RiskMeasurementQuestionEntity]:
        return self.risk_measurement_question_dal.order_by(
            self.risk_measurement_question_dal.all(),
            RiskMeasurementQuestionVo.ORDER
        )

    def submit_attendance(self, member: MemberEntity, answers: List[Dict]) -> None:
        if self.check_attendance_existance(member):
            self._delete_attendance(member)
        for answer in answers:
            filters = {
                RiskMeasurementChoiceVo.ID: answer['choice'],
                f'{RiskMeasurementChoiceVo.QUESTION}__{RiskMeasurementQuestionVo.ID}': answer['question']
            }
            choice = self.risk_measurement_choice_dal.get(**filters)
            self.risk_measurement_vote_dal.create(member=member, choice=choice)

    def get_result(self, member: MemberEntity) -> Dict:
        if has_attended := self.check_attendance_existance(member):
            score = self.get_score(member)
            return {
                RiskMeasurementVo.HAS_ATTENDED: has_attended,
                RiskMeasurementVo.SCORE: score,
                RiskMeasurementVo.DATA: self.SCORE_RESULT_MAPPER[self._get_tolerance(score)]
            }
        else:
            return {RiskMeasurementVo.HAS_ATTENDED: has_attended}

    def get_score(self, member: MemberEntity) -> int:
        filters = {RiskMeasurementVoteVo.MEMBER: member}
        return sum(
            self.risk_measurement_vote_dal.values_list(
                f'{RiskMeasurementVoteVo.CHOICE}__{RiskMeasurementChoiceVo.SCORE}',
                qs=self.risk_measurement_vote_dal.filter(**filters),
                flat=True
            )
        )

    @staticmethod
    def _get_tolerance(score: int) -> RiskToleranceType:
        if score < 10:
            return RiskToleranceType.RISK_AVOIDER
        elif score >= 10 < 20:
            return RiskToleranceType.CATIOUS
        elif score >= 20 < 30:
            return RiskToleranceType.MODERATE
        else:
            return RiskToleranceType.RISK_TAKER

    def check_attendance_existance(self, member: MemberEntity) -> bool:
        filters = {RiskMeasurementVoteVo.MEMBER: member}
        return self.risk_measurement_vote_dal.exists(self.risk_measurement_vote_dal.filter(**filters))

    def _delete_attendance(self, member: MemberEntity) -> None:
        filters = {RiskMeasurementVoteVo.MEMBER: member}
        self.risk_measurement_vote_dal.delete(qs=self.risk_measurement_vote_dal.filter(**filters))
