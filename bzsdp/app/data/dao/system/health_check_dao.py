from bzscl.model.entity.structure.visual_item_entity import VisualItemEntity
from ncl.dal.dao.entity_base_dao import BaseDao
from ncl.utils.common.singleton import Singleton


class HealthCheckDao(BaseDao, metaclass=Singleton):
    model_class = VisualItemEntity
