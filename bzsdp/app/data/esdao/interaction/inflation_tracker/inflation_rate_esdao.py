from typing import List
from ncl.dal.esdao.base_esdao import BaseESDao
from ncl.utils.common.singleton import Singleton
from bzsdp.project.config import BZSDPConfig
from bzsdp.app.model.vo.elasticsearch.elasticsearch_response_vo import ElasticSearchResponseVo


class InflationRateESDao(BaseESDao, metaclass=Singleton):
    INFLATION_RATE_INDEX_NAME = BZSDPConfig.INFLATION_RATE_LIST_ES_INDEX_NAME

    def get_inflation_rates(self) -> List:
        response = self.client.search(index=self.INFLATION_RATE_INDEX_NAME, query=None, size=100)  # change size if needed
        return response[ElasticSearchResponseVo.HITS][ElasticSearchResponseVo.HITS]
