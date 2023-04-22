import json
from typing import Dict

from ncl.dal.rddao.commons_base_rddao import CommonsBaseRDDao, RDKey
from ncl.utils.common.singleton import Singleton


class HomePageRdDao(CommonsBaseRDDao, metaclass=Singleton):
    HOME_PAGE_KEY = RDKey("HOME_PAGE", 6*60)
    def __init__(self):
        super().__init__()

    def set_home_page(self, home_page:Dict):
        model = json.dumps(home_page)

        self.client.set(self.HOME_PAGE_KEY.key, model, self.HOME_PAGE_KEY.ttl)

    def get_home_page(self):

        return self.client.get(self.HOME_PAGE_KEY.key)
