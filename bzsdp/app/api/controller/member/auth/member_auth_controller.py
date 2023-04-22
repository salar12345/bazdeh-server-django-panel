from rest_framework_simplejwt.views import TokenObtainPairView

from bzsdp.app.api.serializer.member import MemberAuthSerializer


class MemberObtainController(TokenObtainPairView):
    serializer_class = MemberAuthSerializer