from rest_framework.views import APIView, Response
from rest_framework.request import Request
from rest_framework import status
from ncl.utils.common.singleton import Singleton
from bzsdp.app.api.serializer.interaction.search.search_loan_serializer import SearchLoanSerializer
from bzsdp.app.model.vo.interaction.search_vo import SearchVo
from bzsdp.app.adapter.grpc.loan.loan_adapter import LoanAdapter
from bzsdp.app.api.serializer.interaction.search.loan_list_proto_serializer import LoanListProtoSerializer
from bzsdp.app.model.vo.content.loan_vo import LoanVO


class SearchLoanController(APIView, metaclass=Singleton):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.adapter = LoanAdapter()

    def get(self, request: Request) -> Response:
        serializer = SearchLoanSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        search_query = serializer.data.get(SearchVo.QUERY_STRING)

        loan_list_response = self.adapter.search_loan_by_name(name=search_query)
        serialized_loan_list = LoanListProtoSerializer(message=loan_list_response)
        return Response(serialized_loan_list.initial_data.get(LoanVO.LOAN_LIST), status=status.HTTP_200_OK)
