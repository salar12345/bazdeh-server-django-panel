import grpc
from bzscl.proto.bazdeh.media.loan import loan_pb2_grpc, loan_pb2
from ncl.utils.common.lru_ttl_cache import lru_ttl_cache
from ncl.utils.common.singleton import Singleton
from bzsdp.project.config import BZSDPConfig


class LoanAdapter(metaclass=Singleton):
    def __init__(self):
        super().__init__()

    @lru_ttl_cache(ttl_seconds=60 * 60 * 24)
    def get_loan_list(self):
        with grpc.insecure_channel(BZSDPConfig.LOAN_SERVE_ADDRESS) as channel:
            stub = loan_pb2_grpc.LoanServeStub(channel=channel)
            request = loan_pb2.GetLoansListQuery()
            responses = stub.GetLoansList(request)

        return responses

    @lru_ttl_cache(ttl_seconds=60 * 60 * 24, maxsize=1000)
    def get_single_loan(self, loan_id=str):
        with grpc.insecure_channel(BZSDPConfig.LOAN_SERVE_ADDRESS) as channel:
            stub = loan_pb2_grpc.LoanServeStub(channel=channel)
            request = loan_pb2.GetSingleLoanQuery(loan_id=loan_id)
            response = stub.GetSingleLoan(request)

        return response

    @lru_ttl_cache(ttl_seconds=60 * 60 * 24, maxsize=1000)
    def get_related_loan(self, loan_amount=int, profit=int, num_of_installment=int):
        with grpc.insecure_channel(BZSDPConfig.LOAN_SERVE_ADDRESS) as channel:
            stub = loan_pb2_grpc.LoanServeStub(channel=channel)
            request = loan_pb2.GetRelatedListQuery(profit_integer=profit, max_loan_integer=loan_amount,
                                                   maximum_payment_time_integer=num_of_installment)
            response = stub.GetRelatedList(request)

        return response

    @lru_ttl_cache(ttl_seconds=60 * 60 * 24, maxsize=1000)
    def search_loan_by_name(self, name: str):
        with grpc.insecure_channel(BZSDPConfig.LOAN_SERVE_ADDRESS) as channel:
            stub = loan_pb2_grpc.LoanServeStub(channel=channel)
            request = loan_pb2.LoanSearchQuery(name=name)
            responses = stub.GetLoanSearch(request)

        return responses
