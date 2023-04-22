from bzscl.utils.grpc_utils.grpc_utils import GrpcUtils
from ncl.utils.common.singleton import Singleton
from ngl.utils.cache.amalgam_cache import AmalgamCache
from ntl.model.amalgam.priceable_enums import AFRAEcoPriceableType
from ntl.model.amalgam.priceable_pair_type import AFRAPriceablePairType
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from bzsdp.app.api.controller.base_api_view import BasePanelController
from bzsdp.app.api.serializer.interaction.gold_bubble_serializer import GoldBubbleSerializer
from bzsdp.app.logic.interaction.interaction_logic import InteractionLogic
from bzsdp.app.model.vo.interaction.interaction_vo import InteractionVO
from bzsdp.project.config import BZSDPConfig


class GoldBubbleController(BasePanelController, APIView, metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.grpc_utils = GrpcUtils()
        self.amalgam_cache = AmalgamCache()
        self.logic = InteractionLogic()

    def post(self, request):
        bubble_variables = request.data
        serializer = GoldBubbleSerializer(data=bubble_variables)
        if serializer.is_valid():
            gold_bubble_respose_dict = {}

            coin_weight = self.logic.determine_coin_weight(target_uri=serializer.data[InteractionVO.COIN_TYPE])

            gold_inherent, gold_bubble = self.logic.calculate_gold_bubble(
                gold_ounce_price=serializer.data[InteractionVO.GOLD_OUNCE_PRICE],
                dollar_price=serializer.data[InteractionVO.DOLLAR_PRICE],
                right_to_mint_coin=serializer.data[InteractionVO.RIGHT_TO_MINT_COIN],
                coin_weight=coin_weight,
                coin_price=serializer.data[InteractionVO.COIN_PRICE])

            gold_bubble_respose_dict[InteractionVO.BUBBLE_PRICE] = gold_bubble
            gold_bubble_respose_dict[InteractionVO.GOLD_INHERENT] = gold_inherent
            return Response(gold_bubble_respose_dict, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        try:
            default_dic = dict()
            default_dic[InteractionVO.RIGHT_TO_MINT_COIN] = int(BZSDPConfig.RIGHT_TO_MINT_COIN)
            default_priceables_list = list()

            default_priceables_list.append(AFRAEcoPriceableType.PC_GOLD_OUNCE.db_value)
            default_priceables_list.append(AFRAEcoPriceableType.C_USD.db_value)
            default_priceables_list.append(AFRAEcoPriceableType.PC_GOLD_COIN_BAHAR.db_value)

            priceable_pair_uris = self.grpc_utils.change_to_priceable_enums(uri_targets=default_priceables_list)

            cache_result = self.amalgam_cache.get_changes(last_read_from_now_seconds=None,
                                                          priceable_pair_codes=set(priceable_pair_uris))

            default_price_target_uri_list = list()
            for result in cache_result:
                default_price_per_target_uri_dict = {}
                first_side_code = AFRAPriceablePairType.find_by_value(result.enum_value.name).first_side.db_value

                default_price_per_target_uri_dict[InteractionVO.TARGET_URI] = first_side_code
                default_price_per_target_uri_dict[InteractionVO.PRICE] = result.price
                default_price_per_target_uri_dict[InteractionVO.YESTERDAY_PRICE] = result.yesterday_closing_price

                default_price_target_uri_list.append(default_price_per_target_uri_dict)

            default_dic[InteractionVO.DEFAULT_PRICE_LIST] = default_price_target_uri_list

            default_coin_types_list = [AFRAEcoPriceableType.PC_GOLD_COIN_BAHAR.db_value,
                                       AFRAEcoPriceableType.PC_GOLD_COIN_HALF.db_value,
                                       AFRAEcoPriceableType.PC_GOLD_COIN_EMAMI.db_value,
                                       AFRAEcoPriceableType.PC_GOLD_COIN_QUARTER.db_value,
                                       AFRAEcoPriceableType.PC_GOLD_COIN_ONE_GRAM.db_value]

            default_dic[InteractionVO.COIN_TYPES_LIST] = default_coin_types_list

            return Response(default_dic, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
