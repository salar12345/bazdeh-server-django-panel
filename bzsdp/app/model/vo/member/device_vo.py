from bzsdp.app.model.vo.base_vo import BaseVO


class DeviceVO(BaseVO):
    GPS_ADID = 'gps_adid'
    IDFA = 'idfa'
    OS_TYPE = 'os_type'
    DEVICE_TYPE = 'device_type'
    APP_VERSION = 'app_version'
    OS_VERSION = 'os_version'
    PUSH_TOKEN = 'push_token'
    DEVICE_MANUFACTURER = 'device_manufacturer'
    DEVICE_MODEL_NAME = 'device_model_name'
    LAST_DB_RESET_TIME = 'last_db_reset_time'
    PACKAGE_NAME = 'package_name'
