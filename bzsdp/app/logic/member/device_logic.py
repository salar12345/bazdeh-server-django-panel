from bzscl.model.entity.member.device_entity import DeviceEntity
from ncl.utils.common.singleton import Singleton
from rest_framework.utils.serializer_helpers import ReturnDict

from bzsdp.app.data.dal.member.device_dal import DeviceDal
from bzsdp.app.model.vo.member.device_vo import DeviceVO


class DeviceLogic(metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.dal = DeviceDal()

    def save_or_update_davice_info(self, device_info: ReturnDict) -> DeviceEntity:
        device = self.get_device_by_gps_adid(gps_adid=device_info.get(DeviceVO.GPS_ADID))
        if device:

            return self.dal.update_device(device_info=device_info, device=device)
        else:
            return self.dal.save_device(device_info=device_info)

    def get_device_by_gps_adid(self, gps_adid: str) -> DeviceEntity:
        return self.dal.get_device_by_gps_adid(gps_adid=gps_adid)
