from ncl.utils.common.singleton import Singleton
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from bzsdp.app.adapter.grpc.deposit.deposit_adapter import DepositAdapter
from bzsdp.app.api.controller.base_api_view import BasePanelController
from bzsdp.app.api.serializer.content.deposit.deposit_list_serializer import DepositListSerializer
from bzsdp.app.api.serializer.content.deposit.related_deposit_request_serializer import RelatedDepositRequestSerializer

from bzsdp.app.logic.content.content_logic import ContentLogic

from bzsdp.app.model.vo.content.deposit_vo import DepositVO


class RelatedDepositController(BasePanelController, APIView, metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.adapter = DepositAdapter()
        self.logic = ContentLogic()

    def post(self, request):
        data = request.data

        serializer = RelatedDepositRequestSerializer(data=data)
        if serializer.is_valid():
            profit = serializer.data.get(DepositVO.PROFIT)
            minimum_inventory = serializer.data.get(DepositVO.MINIMUM_INVENTORY)
            related_deposits = self.adapter.get_related_deposit(profit=profit,minimum_inventory=minimum_inventory)
            serialized_response = DepositListSerializer(message=related_deposits)


            try:
                return Response(serialized_response.initial_data, status=status.HTTP_200_OK)
            except:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
