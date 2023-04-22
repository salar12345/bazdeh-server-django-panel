from typing import List
from ncl.dal.esdao.base_esdao import BaseESDao
from ncl.utils.common.singleton import Singleton
from bzsdp.project.config import BZSDPConfig
from bzsdp.app.model.vo.elasticsearch.elasticsearch_response_vo import ElasticSearchResponseVo


class PriceablesListESDao(BaseESDao, metaclass=Singleton):
    INDEX_NAME = BZSDPConfig.PRICEABLES_LIST_ES_INDEX_NAME

    def get_priceables_list(self) -> List:
        response = self.client.search(index=self.INDEX_NAME, query=None, size=50)  # change size if needed
        return response[ElasticSearchResponseVo.HITS][ElasticSearchResponseVo.HITS]
