from bzscl.model.entity.member.member_entity import MemberEntity
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class MemberAuthSerializer(TokenObtainPairSerializer):



    def validate(self, attrs):
        # authenticate_kwargs = {
        #     self.username_field: attrs[self.username_field],
        #     "password": attrs["password"],
        # }
        # try:
        #     authenticate_kwargs["request"] = self.context["request"]
        # except KeyError:
        #     pass
        #
        # self.user = authenticate(**authenticate_kwargs)
        #
        # if not api_settings.USER_AUTHENTICATION_RULE(self.user):
        #     raise exceptions.AuthenticationFailed(
        #         self.error_messages["no_active_account"],
        #         "no_active_account",
        #     )
        #
        # refresh = self.get_token(self.user)
        #
        # data["refresh"] = str(refresh)
        # data["access"] = str(refresh.access_token)
        #
        # if api_settings.UPDATE_LAST_LOGIN:
        #     update_last_login(None, self.user)



        return None



    @classmethod
    def get_token(cls, member: MemberEntity):
        token = super().get_token(member)

        # Add custom claims
        token['name'] = member.name
        # ...

        return token
