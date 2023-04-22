from typing import Any, Dict, List, Optional

from elastic_transport import ObjectApiResponse
from ncl.dal.esdao.base_esdao import BaseESDao
from ncl.utils.common.singleton import Singleton

from bzsdp.app.model.vo.elasticsearch.elasticsearch_response_vo import ElasticSearchResponseVo
from bzsdp.project.config import BZSDPConfig


class HomePriceESDao(BaseESDao, metaclass=Singleton):
    INDEX_NAME = BZSDPConfig.CONTENT_HOUSING_HOME_PRICE_ES_INDEX_NAME

    def search(
            self,
            query: Optional[Dict] = None,
            fields: Optional[List] = None,
            source: Optional[Any] = None,
            source_excludes: Optional[List] = None,
            size: Optional[int] = None
    ) -> ObjectApiResponse:
        return self.client.search(
            index=self.INDEX_NAME,
            query=query,
            fields=fields,
            source=source,
            source_excludes=source_excludes,
            size=size
        )

    def search_start_end_time(self, query: dict):
        response = self.search_by_query(query=query)[0].get(ElasticSearchResponseVo.SOURCE)

        return response

    def search_two_latest(self, query: dict):
        response = self.search_by_query(query=query)
        last = response[0].get(ElasticSearchResponseVo.SOURCE)
        prev = response[1].get(ElasticSearchResponseVo.SOURCE)
        return last, prev

    def search_by_query(self, query: dict):
        response = self.client.search(body=query, index=self.INDEX_NAME).body.get(ElasticSearchResponseVo.HITS).get(
            ElasticSearchResponseVo.HITS)
        return response
