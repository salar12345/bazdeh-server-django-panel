from bzscl.model.entity.member.member_entity import MemberEntity
from bzscl.model.entity.structure.ab_test_config_entity import AbTestConfigEntity
from ncl.utils.common.singleton import Singleton

from bzsdp.app.data.dao.system.structure_dao import StructureDao


class StructureDal(metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.dao = StructureDao()

    def get_ab_test_active_configs(self, member: MemberEntity):
        return self.dao.get_ab_test_active_configs(member=member)

    def get_active_configs(self):
        return self.dao.get_active_configs()

    def save_member_relation_to_config(self,member:MemberEntity, ab_test_config:AbTestConfigEntity):
        return self.dao.save_member_relation_to_config(member=member, ab_test_config=ab_test_config)
