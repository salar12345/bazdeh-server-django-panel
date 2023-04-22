from bzscl.model.entity.member.member_entity import MemberEntity

from rest_framework_simplejwt.settings import api_settings

AUTH_HEADER_TYPES = api_settings.AUTH_HEADER_TYPES


class BasePanelController:

    def get_current_member(self, request) -> MemberEntity:
        return request.user

    def get_current_member_id(self, request) -> str:
        current_member = self.get_current_member(request)
        if current_member:
            return current_member.id

        return None
