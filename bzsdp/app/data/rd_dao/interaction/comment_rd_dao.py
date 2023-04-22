from typing import Any

from ncl.dal.rddao.commons_base_rddao import CommonsBaseRDDao, RDKey
from ncl.utils.common.singleton import Singleton


class CommentRDDao(CommonsBaseRDDao, metaclass=Singleton):
    COMMENT_CACHE_KEY = RDKey('COMMENT_CACHE', 5 * 60)

    def set(self, key: str, value: Any) -> None:
        self.client.set(f'{self.COMMENT_CACHE_KEY.key}:{key}', value, self.COMMENT_CACHE_KEY.ttl)

    def get(self, key: str) -> Any:
        return self.client.get(f'{self.COMMENT_CACHE_KEY.key}:{key}')
