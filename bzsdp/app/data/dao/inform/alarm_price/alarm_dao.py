from uuid import UUID

from bzscl.model.entity.member.member_entity import MemberEntity
from ncl.utils.common.singleton import Singleton

from ncl.dal.dao.entity_base_dao import BaseDao
from bzscl.model.entity.inform.alarm_entity import AlarmEntity
from django.db.models import Q


class AlarmDao(BaseDao, metaclass=Singleton):
    def __init__(self):
        super().__init__()

    def set_price_alarm(self, member: MemberEntity, alarm_price: float, now_price: float,
                        name: str, code: str, parent_code: str, is_repeated: bool, is_notify: bool, is_more_than: bool,
                        set_datetime):
        alarm_model = AlarmEntity(member=member, alarm_price=alarm_price, current_price=now_price, name=name,
                                  code=code, parent_code=parent_code, is_repeated=is_repeated,
                                  is_notify=is_notify, date_time=set_datetime, is_more_than=is_more_than)

        alarm_model.save()

    def change_alarm_activate(self, alarm_id: str):
        alarm_model = AlarmEntity.objects.filter(id=alarm_id).first()
        is_notify = getattr(alarm_model, 'is_notify')
        if is_notify == True:
            alarm_model.is_notify = False
        else:
            alarm_model.is_notify = True
        alarm_model.save()

    def delete_alarm(self, alarm_id):
        alarm_model = AlarmEntity.objects.filter(id=alarm_id)
        alarm_model.delete()

    def edith_price_alarm(self, alarm_id, alarm_price: float, now_price: float,
                          name: str, code: str, parent_code: str, is_repeated: bool, is_notify: bool, set_datetime):
        alarm_model = AlarmEntity.objects.filter(id=alarm_id).first()
        alarm_model.alarm_price = alarm_price
        alarm_model.current_price = now_price
        alarm_model.name = name
        alarm_model.code = code
        alarm_model.parent_code = parent_code
        alarm_model.is_repeated = is_repeated
        alarm_model.is_notify = is_notify
        alarm_model.date_time = set_datetime
        alarm_model.save()

    def get_all_alarms(self, member: MemberEntity):
        all_alarms = AlarmEntity.objects.filter(member_id=member.id)
        return all_alarms

    def change_alarm_repeated(self, alarm_id: str):
        alarm_model = AlarmEntity.objects.filter(id=alarm_id).first()
        is_repeated = getattr(alarm_model, 'is_repeated')
        if is_repeated == True:
            alarm_model.is_repeated = False
        else:
            alarm_model.is_repeated = True
        alarm_model.save()

    def get_by_name_alarms(self, member: MemberEntity, code: str):
        by_name_alarms = AlarmEntity.objects.filter(member_id=member.id, code=code)
        return by_name_alarms

    def get_all_active_alarms(self) -> [AlarmEntity]:
        all_active_alarms = AlarmEntity.objects.filter(is_notify=True).all()
        return all_active_alarms

    def get_disticnt_alarms_code(self, parent_name: str,) -> [str]:

        return [x['code'] for x in AlarmEntity.objects.filter(parent_code=parent_name).distinct('code').values('code')]

    def get_distinct_alarms_code_without_bourse(self, parent_name:str) ->[str]:
        return [x['code'] for x in
                AlarmEntity.objects.filter(~Q(parent_code=parent_name)).distinct('code').values('code')]

    def get_push_token_by_notice_id(self, notice_id):
        member = AlarmEntity.objects.get(id=notice_id).member

        return \
            AlarmEntity.objects.filter(Q(is_notify=True) | Q(is_repeated=True), member=member, )[
                0].member.devices.all()[
                0].push_token

    def change_is_notify_to_True(self, notice_id):
        alarm_object = AlarmEntity.objects.get(id=notice_id)
        alarm_object.is_notify = False
        alarm_object.save()
        return True

    def get_alarm_name(self, notice_id):

        return AlarmEntity.objects.get(id=notice_id)
