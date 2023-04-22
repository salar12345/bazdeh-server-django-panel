from json import dump
from time import time

from ncl.utils.common.singleton import Singleton
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from bzsdp.app.adapter.grpc.deposit.deposit_adapter import DepositAdapter
from bzsdp.app.api.controller.base_api_view import BasePanelController
from bzsdp.app.api.serializer.content.deposit.deposit_list_serializer import DepositListSerializer
from bzsdp.app.logic.content.content_logic import ContentLogic


class DepositListController(BasePanelController, APIView, metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.adapter = DepositAdapter()
        self.logic = ContentLogic()

    def get(self, request):

        try:
            deposits_response = self.adapter.get_deposit_list()
            serialized_deposits = DepositListSerializer(message=deposits_response)
            try:

                return Response(serialized_deposits.initial_data, status=status.HTTP_200_OK)
            except:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
