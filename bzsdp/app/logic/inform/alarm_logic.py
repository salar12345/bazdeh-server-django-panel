import datetime
from time import sleep

from bzscl.model.enum.structure.app_component import ComponentGrandParent
from ngl.utils.cache.amalgam_cache import AmalgamCache
from ngl.utils.cache.instrument_cache import InstrumentCache
from ntl.model.bourse.market_enums import MarketType
from bzscl.model.entity.inform.alarm_entity import AlarmEntity
from ncl.utils.common.singleton import Singleton
from bzscl.model.entity.member.member_entity import MemberEntity

from bzsdp.app.adapter.grpc.ghasedak.ghasedak_adapter import GhasedakAdapter
from bzsdp.app.data.dal.inform.alarm_dal import AlarmDal

from bzscl.utils.grpc_utils.grpc_utils import GrpcUtils as CommonGrpcUtils

from bzsdp.app.logic.inform.price_notification_logic import PriceNoticeLogic
from bzsdp.project.config import BZSDPConfig


class AlarmLogic(metaclass=Singleton):
    target_market_list = {MarketType.BOURSE, MarketType.FARA_BOURSE}

    def __init__(self):
        super().__init__()

        self.dal = AlarmDal()
        self.price_notice_logic = PriceNoticeLogic()
        self.amalgam_cache = AmalgamCache()
        self.instrument_cache = InstrumentCache(NGL_INSTRUMENT_CACHE_GRPC_URL=BZSDPConfig.GRPC_SERVE_HOST_AFRA,
                                                target_market_list=self.target_market_list,
                                                NGL_CACHE_INFO_REFRESH_INTERVAL_SECOND=BZSDPConfig.REFRESH_INTERVAL_SECOND,
                                                HAS_MOST_TRADE_VALUE=True, HAS_MOST_TRADE_VOLUME=True,
                                                HAS_MOST_PRICE_PERCENT_CHANGES=True,
                                                HAS_MOST_MARKET_VALUE=True,
                                                HAS_MOST_INDEX_EFFECT=True,
                                                HAS_MOST_TRADED_PRICE=True,
                                                # target_instrument_isin_list=['']
                                                )
        self.common_grpc_utils = CommonGrpcUtils()
        self.ghasedak_adapter = GhasedakAdapter()

    def set_price_alarm(self, member: MemberEntity, alarm_price: float, now_price: float, name: str,
                        code: str, parent_code: str, is_repeated: bool, is_notify: bool):
        set_datetime = datetime.datetime.now()
        if alarm_price - now_price > 0:
            is_more_than = True
        else:
            is_more_than = False
        self.dal.set_price_alarm(member=member, alarm_price=alarm_price, now_price=now_price,
                                 name=name, code=code,
                                 parent_code=parent_code, is_repeated=is_repeated,
                                 is_notify=is_notify, set_datetime=set_datetime, is_more_than=is_more_than)

    def change_alarm_activate(self, alarm_id: str):
        self.dal.change_alarm_activate(alarm_id=alarm_id)

    def delete_alarm(self, alarm_id):
        self.dal.delete_alarm(alarm_id=alarm_id)

    def edith_price_alarm(self, alarm_id, alarm_price: float, now_price: float, name: str,
                          code: str, parent_code: str, is_repeated: bool, is_notify: bool):
        set_datetime = datetime.datetime.now()
        self.dal.edith_price_alarm(alarm_id=alarm_id, alarm_price=alarm_price, now_price=now_price,
                                   name=name, code=code,
                                   parent_code=parent_code, is_repeated=is_repeated,
                                   is_notify=is_notify, set_datetime=set_datetime)

    def get_all_alarms(self, member: MemberEntity):
        return self.dal.get_all_alarms(member=member)

    def change_alarm_repeated(self, alarm_id: str):
        self.dal.change_alarm_repeated(alarm_id=alarm_id)

    def get_by_name_alarms(self, member: MemberEntity, code: str):
        return self.dal.get_by_name_alarms(member=member, code=code)

    def get_all_active_alarms(self) -> [AlarmEntity]:
        return self.dal.get_all_active_alarms()

    def get_notify_alarms(self):
        all_instruments_codes = self.dal.get_distinct_alarms_code(parent_name="BZ_BOURSE")
        all_amalgam_codes = self.dal.get_distinct_alarms_code_without_bourse(parent_name="BZ_BOURSE")

        all_notices = []
        for instrument in all_instruments_codes:
            live_price_instrument = self.instrument_cache.get_changes(last_read_from_now_seconds=None,
                                                                      instrument_isins=set(
                                                                          [instrument])).pop().last_traded_price.value
            notices = self.price_notice_logic.observe(instrument_id=str(instrument),
                                                      current_price=live_price_instrument)
            all_notices = all_notices + notices

        for amalgam in all_amalgam_codes:
            priceable_pair_uris = self.common_grpc_utils.change_to_priceable_enums(uri_targets=[amalgam])
            live_price_amalgam = self.amalgam_cache.get_changes(last_read_from_now_seconds=None,
                                                                priceable_pair_codes=priceable_pair_uris).pop().price
            self.price_notice_logic.observe(instrument_id=str(amalgam), current_price=1)
            self.price_notice_logic.observe(instrument_id=str(amalgam), current_price=10000000)
            sleep(2)
            notices = self.price_notice_logic.observe(instrument_id=str(amalgam), current_price=live_price_amalgam)
            all_notices = all_notices + notices

        return all_notices

    def send_inform_alarm(self):
        all_notices = self.get_notify_alarms()

        for notice in all_notices:
            notice_id = notice.notice_id
            try:
                push_token = self.dal.get_push_token_by_notice_id(notice_id=notice_id)
                alarm = self.dal.get_alarm_name(notice_id=notice_id)
                name=alarm.name
                is_more_than = alarm.is_more_than
                if is_more_than:
                    fa_more_than = 'پایین‌تر'
                else:
                    fa_more_than = 'بالاتر'
                price = alarm.alarm_price

                self.dal.change_is_notify_to_True(notice_id=notice_id)
                self.ghasedak_adapter.send_ghasedak_notification(
                    push_token_list=[push_token], title=alarm.name, content=f' قیمت '
                                                                            f'{name} به {fa_more_than} از {price}رسید ',
                    grand_parent=ComponentGrandParent.BZ_MARKET_VIEW, child=notice.instrument_id)
            except:
                continue