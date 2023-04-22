from typing import List

from bzsdp.project.config import BZSDPConfig
from ncl.utils.common.singleton import Singleton
from ngl.protos.afra import instrument_pb2_grpc, instrument_pb2
import grpc


class InstrumentPriceAdapter(metaclass=Singleton):

    def __init__(self):
        super().__init__()

    def get_isin_info(self, isin_list: List):
        channel = grpc.insecure_channel(BZSDPConfig.GRPC_SERVE_HOST_AFRA)
        stub = instrument_pb2_grpc.InstrumentStub(channel)

        live_price = stub.SearchInstrumentInfo(
            instrument_pb2.SearchInstrumentInfoQuery(isin_list=isin_list, market_list=[2], validity_type=1))

        return live_price
