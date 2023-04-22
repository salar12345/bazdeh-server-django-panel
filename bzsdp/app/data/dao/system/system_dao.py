from datetime import datetime
from bzscl.model.entity.structure.force_update_entity import ForceUpdateEntity
from bzscl.model.entity.structure.visual_item_entity import VisualItemEntity
from bzscl.model.entity.system.system_config_entity import SystemConfigEntity
from ncl.utils.common.singleton import Singleton
from ncl.dal.dao.entity_base_dao import BaseDao


class SystemDao(BaseDao, metaclass=Singleton):
    def __init__(self):
        super().__init__()

    def get_all_configs(self):
        return SystemConfigEntity.objects.all()

    def get_needed_configs(self, last_update_time: datetime):
        return SystemConfigEntity.objects.filter(last_update_time__gt=last_update_time)


    def get_needed_visual_item(self, last_update_time: datetime):
        return VisualItemEntity.objects.filter(last_update_time__gt=last_update_time)

    def get_all_visual_item(self):
        return VisualItemEntity.objects.all()
