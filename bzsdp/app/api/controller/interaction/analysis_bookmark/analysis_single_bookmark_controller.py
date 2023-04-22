from ncl.utils.common.singleton import Singleton

from rest_framework.views import APIView

from bzsdp.app.api.controller.base_api_view import BasePanelController


class AnalysisSingleBookmarkController(BasePanelController, APIView, metaclass=Singleton):
    def __init__(self):
        super().__init__()


    def post(self, request):
        pass

