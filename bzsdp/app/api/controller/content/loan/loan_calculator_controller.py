from ncl.utils.common.singleton import Singleton
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from bzsdp.app.api.controller.base_api_view import BasePanelController
from bzsdp.app.api.serializer.content.loan.loan_calculator_request_serializer import LoanCalculatorRequestSerializer
from bzsdp.app.api.serializer.content.loan.related_loan_serializer import RelatedLoanSerializer
from bzsdp.app.logic.content.content_logic import ContentLogic
from bzsdp.app.adapter.grpc.loan.loan_adapter import LoanAdapter
from bzsdp.app.model.vo.content.loan_vo import LoanVO


class LoanCalculatorController(BasePanelController, APIView, metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.adapter = LoanAdapter()
        self.logic = ContentLogic()

    def post(self, request):
        data = request.data

        serializer = LoanCalculatorRequestSerializer(data=data)
        if serializer.is_valid():
            loan_amount = serializer.data.get(LoanVO.LOAN_AMOUNT)
            profit = serializer.data.get(LoanVO.PROFIT)
            num_of_installment = serializer.data.get(LoanVO.NUM_OF_INSTALLMENT)
            related_loans = self.adapter.get_related_loan(loan_amount=loan_amount, profit=profit,
                                                          num_of_installment=num_of_installment)
            serialized_related_loan = RelatedLoanSerializer(message=related_loans)
            installment_value = self.logic.calculate_installment(loan_amount=loan_amount,
                                                                 profit=profit,
                                                                 num_of_installment=num_of_installment)
            response_dict = {LoanVO.INSTALLMENT_VALUE: installment_value, LoanVO.RELATED_LOAN: serialized_related_loan.initial_data.get(LoanVO.RELATED_LOAN)}

            try:
                return Response(response_dict, status=status.HTTP_200_OK)
            except:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
