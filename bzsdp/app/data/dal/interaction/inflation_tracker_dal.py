from typing import List, Dict
from bzsdp.app.data.esdao.interaction.inflation_tracker.inflation_tracker_esdao import InflationTrackerESDao
from ncl.utils.common.singleton import Singleton


class InflationTrackerDal(metaclass=Singleton):
    def __init__(self) -> None:
        self.esdao = InflationTrackerESDao()

    def get_inflation_tracker_info(self, query: Dict) -> List:
        return self.esdao.get_inflation_tracker_info(query)

    def get_list_of_dollar_prices(self, query: Dict) -> List:
        return self.esdao.get_list_of_dollar_prices(query)
