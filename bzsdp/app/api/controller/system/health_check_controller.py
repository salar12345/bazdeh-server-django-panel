from ncl.utils.common.singleton import Singleton
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from bzsdp.app.logic.system.health_check_logic import HealthCheckLogic


class HealthCheckController(APIView, metaclass=Singleton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logic = HealthCheckLogic()
        self.server = self.logic.get_server()

    def get(self, request: Request) -> Response:
        return self.server.as_drf_view()
