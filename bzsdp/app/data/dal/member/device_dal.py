from typing import Union

from bzscl.model.entity.member.device_entity import DeviceEntity
from ncl.utils.common.singleton import Singleton
from rest_framework.utils.serializer_helpers import ReturnDict
from django.core.exceptions import ObjectDoesNotExist

from bzsdp.app.data.dao.member.device_dao import DeviceDao


class DeviceDal(metaclass=Singleton):

    def __init__(self):
        super().__init__()
        self.dao = DeviceDao()

    def get_device_by_gps_adid(self, gps_adid: str) -> Union[DeviceEntity, None]:
        try:
            return self.dao.get_device_by_gps_adid(gps_adid=gps_adid)
        except ObjectDoesNotExist:
            return None

    def update_device(self, device_info: ReturnDict, device: DeviceEntity) -> DeviceEntity:
        return self.dao.update_device(device_info=device_info, device=device)

    def save_device(self, device_info: ReturnDict) -> DeviceEntity:

        return self.dao.save_device(device_info=device_info)
