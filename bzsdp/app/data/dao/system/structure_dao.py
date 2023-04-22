from bzscl.model.entity.member.member_entity import MemberEntity
from bzscl.model.entity.structure.ab_test_config_entity import AbTestConfigEntity
from ncl.utils.common.singleton import Singleton


class StructureDao(metaclass=Singleton):
    def __init__(self):
        super().__init__()

    @staticmethod
    def get_ab_test_active_configs(member: MemberEntity):
        return AbTestConfigEntity.objects.filter(is_active=True, member=member)

    @staticmethod
    def get_active_configs():
        return AbTestConfigEntity.objects.filter(is_active=True)

    @staticmethod
    def save_member_relation_to_config(member: MemberEntity, ab_test_config: AbTestConfigEntity):
        ab_test_config.objects = True
        try:
            ab_test_config.member.add(member)
        except Exception:
            ab_test_config.objects = False
