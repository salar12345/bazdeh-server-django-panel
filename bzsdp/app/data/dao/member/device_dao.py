from bzscl.model.entity.member.device_entity import DeviceEntity
from bzscl.model.entity.member.member_entity import MemberEntity
from ncl.utils.common.singleton import Singleton
from django.db import DatabaseError
from ncl.dal.dao.entity_base_dao import BaseDao

from bzsdp.app.model.vo.member.device_vo import DeviceVO


class DeviceDao(BaseDao, metaclass=Singleton):
    def __init__(self):
        super().__init__()

    def get_device_by_gps_adid(self, gps_adid: str) -> DeviceEntity:
        return DeviceEntity.objects.get(gps_adid=gps_adid)

    def update_device(self, device_info, device: DeviceEntity) -> DeviceEntity:
        device.gps_adid = device_info.get(DeviceVO.GPS_ADID)
        device.idfa = device_info.get(DeviceVO.IDFA)
        device.os_type = device_info.get(DeviceVO.OS_TYPE)
        device.device_type = device_info.get(DeviceVO.DEVICE_TYPE)
        device.app_version = device_info.get(DeviceVO.APP_VERSION)
        device.os_version = device_info.get(DeviceVO.OS_VERSION)
        device.push_token = device_info.get(DeviceVO.PUSH_TOKEN)
        device.device_manufacturer = device_info.get(DeviceVO.DEVICE_MANUFACTURER)
        device.device_model_name = device_info.get(DeviceVO.DEVICE_MODEL_NAME)
        device.last_db_reset_time = device_info.get(DeviceVO.LAST_DB_RESET_TIME)
        device.package_name = device_info.get(DeviceVO.PACKAGE_NAME)
        device.objects = True
        try:
            device.save()
            return device
        except DatabaseError:
            device.active = False
            return device

    def save_device(self, device_info) -> DeviceEntity:

        device = DeviceEntity(gps_adid=device_info.get(DeviceVO.GPS_ADID),
                              idfa=device_info.get(DeviceVO.IDFA),
                              os_type=device_info.get(DeviceVO.OS_TYPE),
                              device_type=device_info.get(DeviceVO.DEVICE_TYPE),
                              app_version=device_info.get(DeviceVO.APP_VERSION),
                              os_version=device_info.get(DeviceVO.OS_VERSION),
                              push_token=device_info.get(DeviceVO.PUSH_TOKEN),
                              device_manufacturer=device_info.get(DeviceVO.DEVICE_MANUFACTURER),
                              device_model_name=device_info.get(DeviceVO.DEVICE_MODEL_NAME),
                              last_db_reset_time=device_info.get(DeviceVO.LAST_DB_RESET_TIME),
                              package_name=device_info.get(DeviceVO.PACKAGE_NAME))

        device.objects = True
        try:
            member = MemberEntity.objects.create(phone_number='', name='', email='')
            device.save()

            member.objects = True
            try:
                member.devices.add(device)
                member.save()
            except DatabaseError:
                member.active = False
            return device
        except DatabaseError:
            device.active = False
            return device
