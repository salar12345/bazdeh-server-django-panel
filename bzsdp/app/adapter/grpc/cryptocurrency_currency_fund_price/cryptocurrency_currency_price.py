from typing import List

from ncl.utils.common.singleton import Singleton
from ngl.protos.afra import amalgam_v_2_pb2_grpc, amalgam_v_2_pb2
import grpc

from bzsdp.project.config import BZSDPConfig


class CurrencyCryptoCurrencyFundPriceAdapter(metaclass=Singleton):

    def get_currency_cryptocurrency_live_price(self, target_uri_list: List):
        with grpc.insecure_channel(BZSDPConfig.GRPC_SERVE_HOST_AFRA) as channel:
            stub = amalgam_v_2_pb2_grpc.AmalgamV2Stub(channel)

            live_price, call = stub.GetLastPrice.with_call(
                amalgam_v_2_pb2.CryptoCurrencyQuery(code_list=target_uri_list))

            return live_price

    def get_fund_info(self, fund_code: List):
        with grpc.insecure_channel(BZSDPConfig.GRPC_SERVE_HOST_AFRA) as channel:
            stub = amalgam_v_2_pb2_grpc.AmalgamV2Stub(channel)

            fund_info, call = stub.GetFundsInfo.with_call(amalgam_v_2_pb2.FundsInfoQuery(code_list=fund_code))

            return fund_info
