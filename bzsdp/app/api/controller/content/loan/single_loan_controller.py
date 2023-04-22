from ncl.utils.common.singleton import Singleton
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from bzsdp.app.api.controller.base_api_view import BasePanelController
from bzsdp.app.api.serializer.content.loan.single_loan_request_serializer import SingleLoanRequesterializer
from bzsdp.app.api.serializer.content.loan.single_loan_response_serializer import SingleLoanResponseSerializer
from bzsdp.app.logic.content.content_logic import ContentLogic

from bzsdp.app.adapter.grpc.loan.loan_adapter import LoanAdapter
from bzsdp.app.model.vo.content.loan_vo import LoanVO


class SingleLoanController(BasePanelController, APIView, metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.adapter = LoanAdapter()
        self.logic = ContentLogic()

    def post(self, request):
        data = request.data
        serializer = SingleLoanRequesterializer(data=data)
        if serializer.is_valid():
            loan_id = serializer.data.get(LoanVO.LOAN_ID)
            single_loan = self.adapter.get_single_loan(loan_id=loan_id)
            try:

                serialized_loan = SingleLoanResponseSerializer(message=single_loan)

                return Response(serialized_loan.initial_data.get(LoanVO.SINGLE_LOAN), status=status.HTTP_200_OK)
            except:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


