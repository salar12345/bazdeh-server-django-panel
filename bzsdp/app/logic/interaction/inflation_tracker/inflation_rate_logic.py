from ncl.utils.common.singleton import Singleton
from bzsdp.app.data.dal.interaction.inflation_rate_dal import InflationRateDal
from typing import List
from bzsdp.app.model.vo.elasticsearch.elasticsearch_response_vo import ElasticSearchResponseVo
from bzsdp.app.model.vo.interaction.inflation_tracker_vo import InflationTrackerVO


class InflationRateLogic(metaclass=Singleton):

    def __init__(self):
        super().__init__()
        self.dal = InflationRateDal()

    def get_inflation_rate_list(self) -> List:
        response = self.dal.get_inflation_rates()
        return self._make_list_of_inflation_rate(response)

    def _make_list_of_inflation_rate(self, response: List) -> List:
        list_of_inflation_rate = []

        for inflation_item in response:
            inflation_dict = {}
            inflation = inflation_item[ElasticSearchResponseVo.SOURCE]

            inflation_dict[InflationTrackerVO.YEAR] = inflation[InflationTrackerVO.YEAR]
            inflation_dict[InflationTrackerVO.INFLATION_RATE] = inflation[InflationTrackerVO.INFLATION_RATE]

            list_of_inflation_rate.append(inflation_dict)

        return list_of_inflation_rate
