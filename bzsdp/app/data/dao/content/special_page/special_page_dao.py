from bzscl.model.entity.content.special_page_entity import SpecialPageEntity

from ncl.dal.dao.entity_base_dao import BaseDao
from ncl.utils.common.singleton import Singleton


class SpecialPageDao(BaseDao, metaclass=Singleton):

    def __init__(self):
        super().__init__()

    def get_all_special_page_subjects(self):
        all_special_page_subjects = SpecialPageEntity.objects.all()
        return all_special_page_subjects
