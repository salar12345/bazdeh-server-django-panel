from ncl.utils.common.singleton import Singleton
from ncl.utils.helper.commons_utils import CommonsUtils

from ngl.protos.afra.amalgam_v_2_pb2 import CarPriceType






from bzsdp.app.model.vo.content.car_price_vo import CarPriceVO


class GrpcUtils(CommonsUtils):
    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def transfer_afra_car_price_type_to_string(cls, car_price_type: CarPriceType = None):

        if car_price_type == CarPriceType.all:
            return CarPriceVO.all

        elif car_price_type == CarPriceType.bazaar:
            return CarPriceVO.bazaar

        elif car_price_type == CarPriceType.namayandegi:
            return CarPriceVO.namayandegi

