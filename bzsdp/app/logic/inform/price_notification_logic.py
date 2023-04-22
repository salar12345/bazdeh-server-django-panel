from typing import List

from ncl.utils.helper.common_price_notice_utils import PriceNoticeConfig, CommonPriceNoticeUtils

from bzsdp.app.data.dal.inform.alarm_dal import AlarmDal


class PriceNoticeLogic(CommonPriceNoticeUtils):

    def __init__(self) -> None:
        super().__init__()


    def find_all_applicable_notice_configs(self) -> List[PriceNoticeConfig]:

        all_alarms = AlarmDal().get_all_active_alarms()
        configs = []

        for alarm in all_alarms:

            alarm_id = alarm.id
            alarm_price = alarm.alarm_price
            current_price = alarm.current_price
            alarm_code = alarm.code
            if alarm_price > current_price:
                upward = True
            else:
                upward = False

            configs.append(PriceNoticeConfig(str(alarm_id), alarm_code, alarm_price, upward))

        return configs
