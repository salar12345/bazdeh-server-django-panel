from ncl.utils.common.singleton import Singleton
from ngl.utils.cache.amalgam_cache import AmalgamCache
from ntl.model.amalgam.priceable_enums import AFRAEcoPriceableType
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from bzsdp.app.api.controller.base_api_view import BasePanelController
from bzsdp.app.api.serializer.interaction.gold_calculator_serializer import GoldCalculatorSerializer
from bzsdp.app.logic.interaction.interaction_logic import InteractionLogic
from bzsdp.app.model.vo.interaction.interaction_vo import InteractionVO
from bzscl.utils.grpc_utils.grpc_utils import GrpcUtils

from bzsdp.project.config import BZSDPConfig


class GoldCalculatorController(BasePanelController, APIView, metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.amalgam_cache = AmalgamCache()
        self.grpc_utils = GrpcUtils()
        self.logic = InteractionLogic()

    def post(self, request):
        calculator_data = request.data
        serializer = GoldCalculatorSerializer(data=calculator_data)

        if serializer.is_valid():
            result = {"price": self.logic.calculate_gold_calculator(serialized_data=serializer)}

            return Response(result, status=status.HTTP_200_OK)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        try:
            model_dict_18 = {}
            model_price_list = []
            model_dict = {}
            model_dict_18[InteractionVO.TARGET_URI] = AFRAEcoPriceableType.PC_GOLD_GRAM_18.db_value
            model_dict_18[InteractionVO.PERSIAN_NAME] = AFRAEcoPriceableType.PC_GOLD_GRAM_18.fa_name
            priceable_pair_uris_18 = self.grpc_utils.change_to_priceable_enums(
                uri_targets=[AFRAEcoPriceableType.PC_GOLD_GRAM_18.db_value])

            price_18 = self.amalgam_cache.get_changes(last_read_from_now_seconds=None,
                                                      priceable_pair_codes=set(priceable_pair_uris_18)).pop()
            model_dict_18[InteractionVO.PRICE] = price_18.price
            model_price_list.append(model_dict_18)
            model_dict_24 = {}
            priceable_pair_uris_24 = self.grpc_utils.change_to_priceable_enums(
                uri_targets=[AFRAEcoPriceableType.PC_GOLD_GRAM_24.db_value])
            price_24 = self.amalgam_cache.get_changes(last_read_from_now_seconds=None,
                                                      priceable_pair_codes=set(priceable_pair_uris_24)).pop()
            model_dict_24[InteractionVO.TARGET_URI] = AFRAEcoPriceableType.PC_GOLD_GRAM_24.db_value
            model_dict_24[InteractionVO.PERSIAN_NAME] = AFRAEcoPriceableType.PC_GOLD_GRAM_24.fa_name
            model_dict_24[InteractionVO.PRICE] = price_24.price
            model_price_list.append(model_dict_24)

            model_dict[InteractionVO.MODEL_PRICE_LIST] = model_price_list
            model_dict[InteractionVO.TAX_DEFAULT] = BZSDPConfig.TAX_DEFAULT
            model_dict[InteractionVO.BENEFIT_DEFAULT] = BZSDPConfig.BENEFIT_DEFAULT
            return Response(model_dict, status=status.HTTP_200_OK)

        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
