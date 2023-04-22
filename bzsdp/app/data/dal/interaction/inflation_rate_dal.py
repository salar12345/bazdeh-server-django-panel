from typing import List
from bzsdp.app.data.esdao.interaction.inflation_tracker.inflation_rate_esdao import InflationRateESDao
from ncl.utils.common.singleton import Singleton


class InflationRateDal(metaclass=Singleton):
    def __init__(self) -> None:
        self.esdao = InflationRateESDao()

    def get_inflation_rates(self) -> List:
        return self.esdao.get_inflation_rates()
