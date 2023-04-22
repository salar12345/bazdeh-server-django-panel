from datetime import datetime

from ncl.utils.common.singleton import Singleton

from bzsdp.app.data.dal.system.system_dal import SystemDal
from bzsdp.app.model.vo.system.system_vo import SystemVO


class SystemLogic(metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.dal = SystemDal()

    def get_all_configs_if_needed(self, last_update_time: str):
        try:
            time_formated = datetime.strptime(last_update_time, SystemVO.APP_CONFIG_AND_VISUAL_ITEM_TIME_FORMAT)
            return self.dal.get_configs_if_needed(last_update_time=time_formated)
        except Exception:
            return self.dal.get_all_configs()

    def get_visual_item(self, last_update_time: str):
        try:
            time_formated = datetime.strptime(last_update_time, SystemVO.APP_CONFIG_AND_VISUAL_ITEM_TIME_FORMAT)
            return self.dal.get_visual_item_if_needed(last_update_time=time_formated)
        except Exception:
            return self.dal.get_all_visual_item()
