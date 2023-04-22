from bzscl.model.entity.inform.alarm_entity import AlarmEntity
from bzscl.model.entity.member.member_entity import MemberEntity
from ncl.utils.common.singleton import Singleton

from bzsdp.app.data.dao.inform.alarm_price.alarm_dao import AlarmDao

class AlarmDal(metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.dao = AlarmDao()

    def set_price_alarm(self, member: MemberEntity, alarm_price: float, now_price: float,
                        name: str, code: str, parent_code: str, is_repeated: bool, is_notify: bool, is_more_than:bool, set_datetime):
        self.dao.set_price_alarm(member=member, alarm_price=alarm_price, now_price=now_price,
                                 name=name, code=code,
                                 parent_code=parent_code, is_repeated=is_repeated,
                                 is_notify=is_notify, set_datetime=set_datetime, is_more_than=is_more_than)

    def change_alarm_activate(self, alarm_id: str):
        self.dao.change_alarm_activate(alarm_id=alarm_id)

    def delete_alarm(self, alarm_id):
        self.dao.delete_alarm(alarm_id=alarm_id)

    def edith_price_alarm(self, alarm_id, alarm_price: float, now_price: float,
                          name: str, code: str, parent_code: str, is_repeated: bool, is_notify: bool, set_datetime):
        self.dao.edith_price_alarm(alarm_id=alarm_id, alarm_price=alarm_price, now_price=now_price,
                                   name=name, code=code,
                                   parent_code=parent_code, is_repeated=is_repeated,
                                   is_notify=is_notify, set_datetime=set_datetime)

    def get_all_alarms(self, member: MemberEntity):
        return self.dao.get_all_alarms(member=member)

    def change_alarm_repeated(self, alarm_id: str):
        self.dao.change_alarm_repeated(alarm_id=alarm_id)

    def get_by_name_alarms(self, member: MemberEntity, code: str):
        return self.dao.get_by_name_alarms(member=member, code=code)

    def get_all_active_alarms(self) -> [AlarmEntity]:
        return self.dao.get_all_active_alarms()

    def get_distinct_alarms_code(self, parent_name):

        return self.dao.get_disticnt_alarms_code(parent_name=parent_name)

    def get_distinct_alarms_code_without_bourse(self, parent_name):
        return self.dao.get_distinct_alarms_code_without_bourse(parent_name=parent_name)

    def get_push_token_by_notice_id(self, notice_id):
        return self.dao.get_push_token_by_notice_id(notice_id=notice_id)

    def change_is_notify_to_True(self, notice_id):
        return self.dao.change_is_notify_to_True(notice_id=notice_id)

    def get_alarm_name(self,notice_id):

        return self.dao.get_alarm_name(notice_id=notice_id)
