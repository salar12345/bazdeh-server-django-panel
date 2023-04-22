import random

from bzscl.model.entity.member.member_entity import MemberEntity
from bzscl.model.entity.structure.ab_test_config_entity import AbTestConfigEntity
from bzscl.model.enum.system.version_type import VersionType
from ncl.utils.common.singleton import Singleton

from bzsdp.app.data.dal.structure.structure_dal import StructureDal
from bzsdp.app.model.vo.system.system_vo import SystemVO


class StructureLogic(metaclass=Singleton):

    def __init__(self):
        super().__init__()
        self.dal = StructureDal()

    def get_ab_test_member_active_config(self, member: MemberEntity):
        struncture_result = self.dal.get_ab_test_active_configs(member).values()[0][SystemVO.VERSION_TYPE]
        result = {}
        result[SystemVO.HOME_PAGE] = struncture_result
        return result

    def determine_version_percentage(self, member: MemberEntity, active_configs: [AbTestConfigEntity]):

        random_int = random.randint(0, 100)
        if active_configs[0].percentage < random_int:
            self.dal.save_member_relation_to_config(member=member, ab_test_config=active_configs[0])
            result = {}
            result[SystemVO.HOME_PAGE] = VersionType.alfa.value
            return result
        else:
            self.dal.save_member_relation_to_config(member=member, ab_test_config=active_configs[1])
            result = {}
            result[SystemVO.HOME_PAGE] = VersionType.beta.value
            return result

    def get_active_configs(self, ):
        return self.dal.get_active_configs()

