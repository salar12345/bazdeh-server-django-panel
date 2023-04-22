from ncl.dal.esdao.base_esdao import BaseESDao
from ncl.utils.common.singleton import Singleton
from bzsdp.project.config import BZSDPConfig
from bzsdp.app.model.vo.elasticsearch.elasticsearch_response_vo import ElasticSearchResponseVo
from typing import Dict


class InflationTrackerESDao(BaseESDao, metaclass=Singleton):
    INFLATION_TRACKER_INDEX_NAME = BZSDPConfig.INFLATION_TRACKER_ES_INDEX_NAME

    def get_inflation_tracker_info(self, query: Dict):
        response = self.client.search(index=self.INFLATION_TRACKER_INDEX_NAME, query=query, size=100)  # change size if needed
        return response[ElasticSearchResponseVo.HITS][ElasticSearchResponseVo.HITS]

    def get_list_of_dollar_prices(self, query: Dict):
        response = self.client.search(index=self.INFLATION_TRACKER_INDEX_NAME, query=query, size=100)  # change size if needed
        return response[ElasticSearchResponseVo.HITS][ElasticSearchResponseVo.HITS]
