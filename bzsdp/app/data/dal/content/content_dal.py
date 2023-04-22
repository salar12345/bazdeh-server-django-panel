from typing import Dict

from ncl.utils.common.singleton import Singleton

from bzsdp.app.data.dao.content.special_page.special_page_dao import SpecialPageDao
from bzsdp.app.data.rd_dao.content.home_page_rd_dao import HomePageRdDao
class ContentDal(metaclass=Singleton):
    def __init__(self):
        self.rd_dao = HomePageRdDao()
        self.dao = SpecialPageDao()

    def cache_home_page(self, home_page: Dict):
        self.rd_dao.set_home_page(home_page=home_page)

    def get_home_page(self):
        return self.rd_dao.get_home_page()

    def get_all_special_page_subjects(self):
        return self.dao.get_all_special_page_subjects()
