from datetime import datetime

from bzscl.model.entity.structure.force_update_entity import ForceUpdateEntity
from ncl.utils.common.singleton import Singleton

from bzsdp.app.data.dao.system.system_dao import SystemDao
from bzsdp.app.data.rd_dao.system.system_rd_dao import SystemRdDao


class SystemDal(metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.dao = SystemDao()
        self.rd_dao = SystemRdDao()

    def get_all_configs(self):
        return self.dao.get_all_configs()

    def get_configs_if_needed(self, last_update_time: datetime):
        return self.dao.get_needed_configs(last_update_time=last_update_time)

    def get_visual_item_if_needed(self, last_update_time: datetime):
        return self.dao.get_needed_visual_item(last_update_time=last_update_time)

    def get_all_visual_item(self):
        return self.dao.get_all_visual_item()
