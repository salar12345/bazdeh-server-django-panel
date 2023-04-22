from ncl.utils.common.singleton import Singleton
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from bzsdp.app.api.controller.base_api_view import BasePanelController
from bzsdp.app.api.serializer.content.home_price.start_and_end_time_home_price_serializer import \
    StartAndEndTimeHomePriceSerializer
from bzsdp.app.logic.content.home_price_logic import HomePriceLogic

class StartAndEndTimeHomePriceController(BasePanelController, APIView, metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.logic = HomePriceLogic()

    def get(self, request):
        try:
            response = self.logic.get_start_and_end_time_home_price()
            try:
                serialized_response = StartAndEndTimeHomePriceSerializer(data=response)
                return Response(serialized_response.initial_data, status=status.HTTP_200_OK)
            except:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)




