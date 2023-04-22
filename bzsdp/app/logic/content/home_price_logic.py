from typing import Dict, List, Optional

from bzscl.model.vo.content.home_price_vo import HomePriceVo
from bzscl.model.enum.content.shamsi_month_type import ShamsiMonthType
from ncl.utils.common.singleton import Singleton

from bzsdp.app.data.dal.content.housing_dal import HomePriceDal
from bzsdp.app.model.vo.elasticsearch.elasticsearch_query_vo import ElasticSearchQueryVo
from bzsdp.app.model.vo.elasticsearch.elasticsearch_response_vo import ElasticSearchResponseVo


class HomePriceLogic(metaclass=Singleton):
    def __init__(self) -> None:
        self.home_price_dal = HomePriceDal()

    @staticmethod
    def _generate_date_bool_query(year: int, month: ShamsiMonthType) -> Dict:
        return {
            ElasticSearchQueryVo.BOOL: {
                ElasticSearchQueryVo.MUST: [
                    {ElasticSearchQueryVo.NESTED: {ElasticSearchQueryVo.PATH: HomePriceVo.home_price_date, ElasticSearchQueryVo.QUERY: {
                        ElasticSearchQueryVo.MATCH: {f'{HomePriceVo.home_price_date}.{HomePriceVo.year}': year}
                    }}},
                    {ElasticSearchQueryVo.NESTED: {ElasticSearchQueryVo.PATH: HomePriceVo.home_price_date, ElasticSearchQueryVo.QUERY: {
                        ElasticSearchQueryVo.MATCH: {f'{HomePriceVo.home_price_date}.{HomePriceVo.month}': month}
                    }}},
                ]
            }
        }

    @staticmethod
    def _extract_single_region_price_from_document(document: Dict, region_name: int) -> Dict:
        for region_price in document[ElasticSearchResponseVo.SOURCE][HomePriceVo.region_price]:
            if region_price[HomePriceVo.region_name] == int(region_name):
                return region_price

    def _create_region_price_list_by_region_name(self, region_name: int) -> List:
        result = list()
        documents = self.home_price_dal.search(None, None, None, None, 10000)
        for document in documents[ElasticSearchResponseVo.HITS][ElasticSearchResponseVo.HITS]:
            region_price = self._extract_single_region_price_from_document(document, region_name)
            result.append(
                {
                    **document[ElasticSearchResponseVo.SOURCE][HomePriceVo.home_price_date],
                    HomePriceVo.average_price: region_price[HomePriceVo.average_price],
                    HomePriceVo.number_of_deals: region_price[HomePriceVo.number_of_deals]
                }
            )
        return result

    # The document is distinguished by it's date, since the date field should be unique in the elastic index
    def _get_region_price_by_document(
            self,
            year: int,
            month: ShamsiMonthType,
    ) -> List:
        query = self._generate_date_bool_query(year, month)
        return self.home_price_dal.search(
            query,
            None,
            None,
            [HomePriceVo.creation_datetime, HomePriceVo.home_price_date],
            10000
        )[ElasticSearchResponseVo.HITS][ElasticSearchResponseVo.HITS][0][ElasticSearchResponseVo.SOURCE][HomePriceVo.region_price]

    @staticmethod
    def _combine_region_prices_of_two_dates(prices: List, previous_prices: Optional[List] = None) -> List:
        results = list()

        if previous_prices:
            for price, previous_price in zip(prices, previous_prices):
                results.append({**price, 'previous_month_price': previous_price[HomePriceVo.average_price]})
            return results

        for price in prices:
            results.append({**price, 'previous_month_price': None})
        return results

    def get_all_region_prices_by_date(self, year: int, month: ShamsiMonthType) -> List:
        prices_for_given_date = self._get_region_price_by_document(year, month)

        try:
            if month.value != 1:
                prices_for_month_before_given_date = self._get_region_price_by_document(
                    year,
                    month.value - 1
                )
            else:
                prices_for_month_before_given_date = self._get_region_price_by_document(
                    year - 1,
                    ShamsiMonthType.ESFAND.value
                )
        except Exception:
            prices_for_month_before_given_date = None

        return self._combine_region_prices_of_two_dates(
            prices_for_given_date,
            prices_for_month_before_given_date
        )

    def get_region_price_history(self, region_name: int) -> List:
        result = list()
        documents = self.home_price_dal.search(None, None, None, None, 10000)
        for document in documents[ElasticSearchResponseVo.HITS][ElasticSearchResponseVo.HITS]:
            region_price = self._extract_single_region_price_from_document(document, region_name)
            result.append(
                {
                    **document[ElasticSearchResponseVo.SOURCE][HomePriceVo.home_price_date],
                    HomePriceVo.average_price: region_price[HomePriceVo.average_price],
                    HomePriceVo.number_of_deals: region_price[HomePriceVo.number_of_deals]
                }
            )
        return result

    def get_start_and_end_time_home_price(self):
        result_dict = {}

        start_time_query = self._create_start_end_time_search_query(ElasticSearchQueryVo.ASC)
        start_time_response = self.home_price_dal.search_start_end_time(query=start_time_query).get(
            HomePriceVo.home_price_date)

        result_dict[HomePriceVo.START_YEAR] = start_time_response.get(HomePriceVo.year)
        start_month = start_time_response.get(HomePriceVo.month)
        result_dict[HomePriceVo.START_MONTH] = ShamsiMonthType[start_month].value
        result_dict[HomePriceVo.START_FA_MONTH] = ShamsiMonthType[start_month].fa_name
        result_dict[HomePriceVo.START_EN_MONTH] = ShamsiMonthType[start_month].en_name
        if result_dict[HomePriceVo.START_MONTH] < 10:
            str_start_month = "0" + str(result_dict[HomePriceVo.START_MONTH])
        else:
            str_start_month = str(result_dict[HomePriceVo.START_MONTH])
        result_dict[HomePriceVo.START_DATE] = str(result_dict[HomePriceVo.START_YEAR]) + "/" + str_start_month + "/01"

        end_time_query = self._create_start_end_time_search_query(ElasticSearchQueryVo.DESC)
        end_time_response = self.home_price_dal.search_start_end_time(query=end_time_query).get(
            HomePriceVo.home_price_date)

        result_dict[HomePriceVo.END_YEAR] = end_time_response.get(HomePriceVo.year)
        end_month = end_time_response.get(HomePriceVo.month)
        result_dict[HomePriceVo.END_MONTH] = ShamsiMonthType[end_month].value
        result_dict[HomePriceVo.END_FA_MONTH] = ShamsiMonthType[end_month].fa_name
        result_dict[HomePriceVo.END_EN_MONTH] = ShamsiMonthType[end_month].en_name
        if result_dict[HomePriceVo.END_MONTH] < 10:
            str_end_month = "0" + str(result_dict[HomePriceVo.END_MONTH])
        else:
            str_end_month = str(result_dict[HomePriceVo.END_MONTH])
        result_dict[HomePriceVo.END_DATE] = str(result_dict[HomePriceVo.END_YEAR]) + "/" + str_end_month + "/30"

        return result_dict


    @staticmethod
    def _create_start_end_time_search_query(mod):
        query = {
            ElasticSearchQueryVo.SIZE: 1,
            ElasticSearchQueryVo.SORT: [
                {
                    f'{HomePriceVo.home_price_date}.{HomePriceVo.year}': {
                        ElasticSearchQueryVo.ORDER: mod,
                        ElasticSearchQueryVo.NESTED: {ElasticSearchQueryVo.PATH: HomePriceVo.home_price_date}
                    }
                },
                {
                    f'{HomePriceVo.home_price_date}.{HomePriceVo.month}': {
                        ElasticSearchQueryVo.ORDER: mod,
                        ElasticSearchQueryVo.NESTED: {ElasticSearchQueryVo.PATH: HomePriceVo.home_price_date}
                    }
                }
            ]
        }
        return query

    def last_home_price_average_price(self):
        home_price = {}
        end_time_query = self._create_two_last_home_price_search_query()
        last_home_price, prev_home_price = self.home_price_dal.search_two_latest(query=end_time_query)
        home_price[HomePriceVo.year] = last_home_price.get(HomePriceVo.home_price_date).get(HomePriceVo.year)
        month = last_home_price.get(HomePriceVo.home_price_date).get(HomePriceVo.month)
        home_price[HomePriceVo.month] = ShamsiMonthType[month].fa_name
        home_price["last_price"] = last_home_price.get(HomePriceVo.region_price)[21].get(HomePriceVo.average_price)
        home_price["prev_price"] = prev_home_price.get(HomePriceVo.region_price)[21].get(HomePriceVo.average_price)
        return home_price

    @staticmethod
    def _create_two_last_home_price_search_query():
        query = {
            ElasticSearchQueryVo.SIZE: 2,
            ElasticSearchQueryVo.SORT: [
                {
                    f'{HomePriceVo.home_price_date}.{HomePriceVo.year}': {
                        ElasticSearchQueryVo.ORDER: ElasticSearchQueryVo.DESC,
                        ElasticSearchQueryVo.NESTED: {ElasticSearchQueryVo.PATH: HomePriceVo.home_price_date}
                    }
                },
                {
                    f'{HomePriceVo.home_price_date}.{HomePriceVo.month}': {
                        ElasticSearchQueryVo.ORDER: ElasticSearchQueryVo.DESC,
                        ElasticSearchQueryVo.NESTED: {ElasticSearchQueryVo.PATH: HomePriceVo.home_price_date}
                    }
                }
            ]
        }
        return query
