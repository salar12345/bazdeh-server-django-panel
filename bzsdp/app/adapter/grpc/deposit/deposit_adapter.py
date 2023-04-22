import grpc
from bzscl.proto.bazdeh.media.deposit import deposit_pb2_grpc, deposit_pb2
from ncl.utils.common.lru_ttl_cache import lru_ttl_cache
from ncl.utils.common.singleton import Singleton
from bzsdp.project.config import BZSDPConfig


class DepositAdapter(metaclass=Singleton):
    def __init__(self):
        super().__init__()

    @lru_ttl_cache(ttl_seconds=60 * 60 * 24 * 2)
    def get_deposit_list(self):
        with grpc.insecure_channel(BZSDPConfig.LOAN_SERVE_ADDRESS) as channel:
            stub = deposit_pb2_grpc.DepositServeStub(channel=channel)
            request = deposit_pb2.DepositListQuery()
            responses = stub.GetDepositList(request)

        return responses

    @lru_ttl_cache(ttl_seconds=60 * 60 * 24 * 2)
    def get_single_deposit(self, deposit_id=str):
        with grpc.insecure_channel(BZSDPConfig.LOAN_SERVE_ADDRESS) as channel:
            stub = deposit_pb2_grpc.DepositServeStub(channel=channel)
            request = deposit_pb2.SingleDepositQuery(deposit_id=deposit_id)
            response = stub.GetSingleDeposit(request)

        return response

    @lru_ttl_cache(ttl_seconds=60 * 60 * 24)
    def get_related_deposit(self, minimum_inventory=int, profit=int):
        with grpc.insecure_channel(BZSDPConfig.LOAN_SERVE_ADDRESS) as channel:
            stub = deposit_pb2_grpc.DepositServeStub(channel=channel)
            request = deposit_pb2.RelatedListQuery(integer_profit=profit, integer_minimum_inventory=minimum_inventory)
            response = stub.GetRelatedList(request)

        return response

    # @lru_ttl_cache(ttl_seconds=60 * 60 * 24)
    def search_on_deposit(self, name: str):
        with grpc.insecure_channel(BZSDPConfig.LOAN_SERVE_ADDRESS) as channel:
            stub = deposit_pb2_grpc.DepositServeStub(channel=channel)
            request = deposit_pb2.StringQuery(query_string=name)
            response = stub.GetDepositByQueryString(request)

        return response

