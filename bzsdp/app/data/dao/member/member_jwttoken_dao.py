from bzscl.model.entity.member.member_entity import MemberEntity
from bzscl.model.entity.member.member_jwttoken_entity import MemberJWTTokenEntity
from ncl.dal.dao.entity_base_dao import BaseDao
from ncl.utils.common.singleton import Singleton


class MemberJWTTokenDao(BaseDao, metaclass=Singleton):
    model_class = MemberJWTTokenEntity

    def get_by_member(self, member: MemberEntity) -> MemberJWTTokenEntity:
        return self.model_class.objects.get(member=member)
