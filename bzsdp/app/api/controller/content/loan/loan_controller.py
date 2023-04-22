from time import time

from ncl.utils.common.singleton import Singleton
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from bzsdp.app.api.controller.base_api_view import BasePanelController
from bzsdp.app.api.serializer.content.loan.loan_list_serializer import LoanListSerializer
from bzsdp.app.logic.content.content_logic import ContentLogic

from bzsdp.app.adapter.grpc.loan.loan_adapter import LoanAdapter
from bzsdp.app.model.vo.content.loan_vo import LoanVO
from bzsdp.shared.metrics.content.loan_mertrics.loan_metrics import LOAN_CONTROLLER_TIME_LATENCY, \
    LOAN_CONTROLLER_NUMBER_OF_OBSERVATION


class LoanController(BasePanelController, APIView, metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.adapter = LoanAdapter()
        self.logic = ContentLogic()

    def get(self, request):

        try:
            start_time = time()
            loans_response = self.adapter.get_loan_list()
            #LOAN_CONTROLLER_NUMBER_OF_OBSERVATION.observe(len())
            serialized_loan = LoanListSerializer(message=loans_response)
            try:
                end_time = time()
                LOAN_CONTROLLER_TIME_LATENCY.observe(end_time - start_time)
                return Response(serialized_loan.initial_data.get(LoanVO.LOAN_LIST), status=status.HTTP_200_OK)
            except:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
