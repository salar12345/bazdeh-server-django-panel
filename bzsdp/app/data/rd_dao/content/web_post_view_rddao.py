from typing import Any

from ncl.dal.rddao.commons_base_rddao import CommonsBaseRDDao
from ncl.utils.common.singleton import Singleton


class WebPostViewRDDao(CommonsBaseRDDao, metaclass=Singleton):
    CACHE_KEY = 'WEB_POST_VIEW_COUNTER'

    def set(self, value: Any) -> None:
        self.client.set(self.CACHE_KEY, value)

    def get(self) -> Any:
        return self.client.get(self.CACHE_KEY)
