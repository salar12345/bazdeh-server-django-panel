from bzscl.model.enum.content.news_general_category_type import NewsGeneralCategoryGroupType
from bzscl.utils.grpc_utils.grpc_utils import GrpcUtils
from ncl.utils.common.singleton import Singleton
from ngl.utils.cache.base_amalgam_cache import BaseAmalgamCache
from ngl.utils.cache.instrument_cache import InstrumentCache
from ntl.model.bourse.market_enums import MarketType
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from bzsdp.app.api.controller.base_api_view import BasePanelController
from bzsdp.app.api.serializer.member.serve_portfolio_serializer import ServePortfolioSerializer

from bzsdp.app.logic.member.member_logic import MemberLogic
from bzsdp.app.model.vo.content.loan_vo import LoanVO
from bzsdp.app.model.vo.member.portfolio_vo import PortfolioVO
from ntl.model.amalgam.priceable_enums import AFRAEcoPriceableType

from bzsdp.project.config import BZSDPConfig


class ServePortfolioController(BasePanelController, APIView, metaclass=Singleton):
    target_market_list = {MarketType.BOURSE, MarketType.FARA_BOURSE}
    NGL_CACHE_INFO_REFRESH_INTERVAL_SECOND = 7200 * 12

    def __init__(self):
        super().__init__()
        self.logic = MemberLogic()
        self.grpc_utils = GrpcUtils()
        self.amalgam_cache = BaseAmalgamCache()
        self.instrument_cache = InstrumentCache(NGL_INSTRUMENT_CACHE_GRPC_URL=BZSDPConfig.GRPC_SERVE_HOST_AFRA,
                                                target_market_list=self.target_market_list,
                                                NGL_CACHE_INFO_REFRESH_INTERVAL_SECOND=self.NGL_CACHE_INFO_REFRESH_INTERVAL_SECOND)

    def get(self, request):
        member = self.get_current_member(request)
        all_assets = self.logic.get_all_assets(member=member)
        afra_peiceables = self.grpc_utils.change_to_priceable_enums(uri_targets=[AFRAEcoPriceableType.C_USD.db_value])
        usd_price = self.amalgam_cache.get_changes(priceable_pair_codes=afra_peiceables).pop().price
        map = {}
        result = []
        for asset in all_assets:
            portfolio_id = asset.portfolio_id
            if map.get(portfolio_id) is None:
                map[portfolio_id] = []
                map[portfolio_id].append(asset)
            else:
                map.get(portfolio_id).append(asset)
        for key, portfolio_assets in map.items():
            base_value = 0
            current_value = 0

            for asset in portfolio_assets:

                if asset.parent_code == NewsGeneralCategoryGroupType.BZ_CURRENCY.value \
                        or asset.parent_code == NewsGeneralCategoryGroupType.BZ_GOLDCOIN.value \
                        or asset.parent_code == NewsGeneralCategoryGroupType.BZ_GOLDANDVALUABLEMETALS.value:
                    try:
                        model = self.amalgam_cache.get_changes(60, self.grpc_utils.change_to_priceable_enums(
                            uri_targets=[asset.code])).pop()
                    except:
                        model = self.amalgam_cache.get_changes(60, self.grpc_utils.change_to_priceable_enums(
                            uri_targets=[asset.code]))
                    current_value += model.price * asset.count
                    base_value += asset.buy_price * asset.count


                elif asset.parent_code == NewsGeneralCategoryGroupType.BZ_CRYPTOCURRENCY.value:
                    model = self.amalgam_cache.get_changes(60, self.grpc_utils.change_to_priceable_enums(
                        uri_targets=[asset.code])).pop()
                    current_value += model.price * usd_price * asset.count
                    base_value += asset.buy_price * asset.daily_usd_price * asset.count


                elif asset.parent_code == NewsGeneralCategoryGroupType.BZ_BOURSE.value \
                        or asset.parent_code == NewsGeneralCategoryGroupType.BZ_FARABOURSE.value:
                    model = self.instrument_cache.find_by_isins({asset.code}).pop()
                    current_value += model.last_traded_price.value * asset.count
                    base_value += asset.buy_price * asset.count

            dict = {PortfolioVO.ID: key,
                    PortfolioVO.CURRENT_VALUE: current_value,
                    PortfolioVO.BASE_VALUE: base_value}
            result.append(dict)

            serialized_result = ServePortfolioSerializer(result, maney=True)
            return Response(serialized_result.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
