from ncl.utils.common.singleton import Singleton
from bzsdp.app.data.dal.interaction.priceables_list_dal import PriceablesListDal
from typing import List
from bzsdp.app.model.vo.elasticsearch.elasticsearch_response_vo import ElasticSearchResponseVo
from bzsdp.app.model.vo.interaction.inflation_tracker_vo import InflationTrackerVO


class PriceablesListLogic(metaclass=Singleton):

    def __init__(self):
        super().__init__()
        self.dal = PriceablesListDal()

    def get_priceables_list(self) -> List:
        response = self.dal.get_priceables()
        return self._make_list_of_priceables(response)

    def _make_list_of_priceables(self, response: List) -> List:
        list_of_priceables = []

        for priceable_item in response:
            priceable_dict = {}
            priceable = priceable_item[ElasticSearchResponseVo.SOURCE]

            priceable_dict[InflationTrackerVO.PRICEABLE_ID] = priceable_item[InflationTrackerVO.ID]
            priceable_dict[InflationTrackerVO.PRICEABLE_NAME] = priceable[InflationTrackerVO.PRICEABLE_NAME]
            priceable_dict[InflationTrackerVO.UNIT] = priceable[InflationTrackerVO.UNIT]
            priceable_dict[InflationTrackerVO.IS_DEFAULT] = priceable[InflationTrackerVO.IS_DEFAULT]
            priceable_dict[InflationTrackerVO.START_YEAR] = self._get_start_or_end_priceable_year(
                priceable[InflationTrackerVO.PRICEABLE_INFO], is_start_year=False
            )
            priceable_dict[InflationTrackerVO.END_YEAR] = self._get_start_or_end_priceable_year(
                priceable[InflationTrackerVO.PRICEABLE_INFO], is_start_year=True
            )

            list_of_priceables.append(priceable_dict)

        return list_of_priceables

    def _get_start_or_end_priceable_year(self, priceable_info: List, is_start_year: bool) -> int:
        if is_start_year:
            return max(priceable_info, key=lambda x: x[InflationTrackerVO.YEAR]).get(InflationTrackerVO.YEAR)
        return min(priceable_info, key=lambda x: x[InflationTrackerVO.YEAR]).get(InflationTrackerVO.YEAR)
