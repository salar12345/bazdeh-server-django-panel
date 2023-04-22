from ncl.utils.common.singleton import Singleton
from bzsdp.app.data.dal.interaction.inflation_tracker_dal import InflationTrackerDal
from typing import List, Dict
from bzsdp.app.model.vo.elasticsearch.elasticsearch_query_vo import ElasticSearchQueryVo
from bzsdp.app.model.vo.elasticsearch.elasticsearch_response_vo import ElasticSearchResponseVo
from bzsdp.app.model.vo.interaction.inflation_tracker_vo import InflationTrackerVO


class InflationTrackerLogic(metaclass=Singleton):

    def __init__(self):
        super().__init__()
        self.dal = InflationTrackerDal()

    def get_inflation_tracker_info(self, priceable_id: str) -> Dict:
        query = self._make_inflation_tracker_info_query(priceable_id)
        inflation_tracker_info = self.dal.get_inflation_tracker_info(query)[0][ElasticSearchResponseVo.SOURCE]

        crypto_currencies = ['بیت‌کوین', 'اتریوم']
        if inflation_tracker_info[InflationTrackerVO.PRICEABLE_NAME] in crypto_currencies:
            inflation_tracker_info[InflationTrackerVO.PRICEABLE_INFO] = self._convert_crypto_currency_to_tomans(
                inflation_tracker_info[InflationTrackerVO.PRICEABLE_INFO])

        return inflation_tracker_info

    def _convert_crypto_currency_to_tomans(self, priceable_info: List) -> List:
        list_of_dollar_prices = self._get_list_of_dollar_prices()
        for data in priceable_info:
            dollar_price = self._get_dollar_price_by_year(list_of_dollar_prices, data[InflationTrackerVO.YEAR])
            float_price = data[InflationTrackerVO.PRICE] * dollar_price
            data[InflationTrackerVO.PRICE] = float(f'{float_price:.2f}')

        return priceable_info

    def _get_list_of_dollar_prices(self) -> List:
        query = self._make_query_to_get_dollar_price_by_year()
        response = self.dal.get_list_of_dollar_prices(query)
        return response[0][ElasticSearchResponseVo.SOURCE][InflationTrackerVO.PRICEABLE_INFO]

    def _get_dollar_price_by_year(self, list_of_dollar_prices: List, year: int) -> float:
        dollar_price = \
        list(filter(lambda priceable: priceable[InflationTrackerVO.YEAR] == year, list_of_dollar_prices))[0][
            InflationTrackerVO.PRICE]
        return dollar_price

    def _make_query_to_get_dollar_price_by_year(self) -> Dict:
        query = dict()
        query[ElasticSearchQueryVo.MATCH] = {
            InflationTrackerVO.PRICEABLE_NAME: {ElasticSearchQueryVo.QUERY: 'دلار'}
        }
        return query

    def _make_inflation_tracker_info_query(self, priceable_id: str) -> Dict:
        query = dict()
        query[ElasticSearchQueryVo.MATCH] = {
            ElasticSearchResponseVo.ID: {ElasticSearchQueryVo.QUERY: f'{priceable_id}'}
        }
        return query
