import grpc
from ncl.utils.common.singleton import Singleton
from ngl.protos.afra import amalgam_v_2_pb2_grpc, amalgam_v_2_pb2
from ngl.protos.afra.amalgam_v_2_pb2 import CarPriceType

from bzsdp.project.config import BZSDPConfig


class CarPriceOldAdapter(metaclass=Singleton):

    def __init__(self):
        super().__init__()

    def get_live_price(self, target_uris: list = [], price_type: CarPriceType = CarPriceType.all,
                                     production_year: int = 0):
        with grpc.insecure_channel(BZSDPConfig.GRPC_SERVE_HOST_AFRA) as channel:
            stub = amalgam_v_2_pb2_grpc.AmalgamV2Stub(channel)

            live_price, call = stub.GetCarLastPrice.with_call(
                amalgam_v_2_pb2.CarLastPriceQuery(car_entity_name=target_uris, price_type=price_type,
                                                  production_year=production_year))

            return live_price
