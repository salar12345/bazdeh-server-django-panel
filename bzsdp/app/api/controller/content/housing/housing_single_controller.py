from bzscl.model.enum.content.tehran_region_type import TehranRegionType
from ncl.utils.common.singleton import Singleton
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from bzsdp.app.logic.content.home_price_logic import HomePriceLogic



class GetSingleHomePriceController(APIView, metaclass=Singleton):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.home_price_logic = HomePriceLogic()

    def post(self, request: Request) -> Response:
        try:
            return Response(
                self.home_price_logic.get_region_price_history(
                    TehranRegionType[request.data['region_name']].numeric
                ),
                HTTP_200_OK
            )
        except Exception:
            return Response(None, HTTP_400_BAD_REQUEST)
