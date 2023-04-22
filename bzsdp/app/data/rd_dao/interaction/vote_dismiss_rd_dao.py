from typing import Any

from ncl.dal.rddao.commons_base_rddao import CommonsBaseRDDao
from ncl.utils.common.singleton import Singleton


class VoteDismissRDDao(CommonsBaseRDDao, metaclass=Singleton):
    CACHE_KEY = 'VOTE_DISMISS'

    def set(self, key: str, value: Any) -> None:
        self.client.set(f'{self.CACHE_KEY}:{key}', value)

    def get(self, key: str) -> Any:
        return self.client.get(f'{self.CACHE_KEY}:{key}')
