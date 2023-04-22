from enum import Enum


class RiskToleranceType(Enum):
    RISK_AVOIDER = 'RISK_AVOIDER'
    CATIOUS = 'CATIOUS'
    MODERATE = 'MODERATE'
    RISK_TAKER = 'RISK_TAKER'
