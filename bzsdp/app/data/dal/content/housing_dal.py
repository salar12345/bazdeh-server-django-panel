from typing import Any, Dict, List, Optional

from elastic_transport import ObjectApiResponse
from bzsdp.app.data.esdao.content.home_price_esdao import HomePriceESDao

from ncl.utils.common.singleton import Singleton


class HomePriceDal(metaclass=Singleton):
    def __init__(self) -> None:
        self.esdao = HomePriceESDao()

    def search(
        self,
        query: Optional[Dict] = None,
        fields: Optional[List] = None,
        source: Optional[Any] = None,
        source_excludes: Optional[List] = None,
        size: Optional[int] = None
    ) -> ObjectApiResponse:
        return self.esdao.search(
            query,
            fields,
            source,
            source_excludes,
            size
        )

    def search_start_end_time(self, query: dict):
        return self.esdao.search_start_end_time(query=query)

    def search_two_latest(self, query: dict):
        return self.esdao.search_two_latest(query=query)
