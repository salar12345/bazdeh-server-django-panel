from ncl.utils.common.singleton import Singleton
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from bzsdp.app.adapter.grpc.deposit.deposit_adapter import DepositAdapter
from bzsdp.app.api.controller.base_api_view import BasePanelController
from bzsdp.app.api.serializer.content.deposit.single_deposit_request_serializer import SingleDepositRequesterializer
from bzsdp.app.api.serializer.content.deposit.single_deposit_response_serializer import SingleDepositResponseSerializer
from bzsdp.app.api.serializer.content.loan.single_loan_request_serializer import SingleLoanRequesterializer
from bzsdp.app.api.serializer.content.loan.single_loan_response_serializer import SingleLoanResponseSerializer
from bzsdp.app.logic.content.content_logic import ContentLogic

from bzsdp.app.adapter.grpc.loan.loan_adapter import LoanAdapter
from bzsdp.app.model.vo.content.deposit_vo import DepositVO
from bzsdp.app.model.vo.content.loan_vo import LoanVO


class SingleDepositController(BasePanelController, APIView, metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.adapter = DepositAdapter()
        self.logic = ContentLogic()

    def post(self, request):
        data = request.data
        serializer = SingleDepositRequesterializer(data=data)
        if serializer.is_valid():
            deposit_id = serializer.data.get(DepositVO.DEPOSIT_ID)
            single_deposit = self.adapter.get_single_deposit(deposit_id=deposit_id)
            try:

                serialized_deposit = SingleDepositResponseSerializer(message=single_deposit)

                return Response(serialized_deposit.initial_data, status=status.HTTP_200_OK)
            except:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


