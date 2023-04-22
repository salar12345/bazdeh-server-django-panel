from functools import lru_cache

from bzscl.model.enum.structure.search_category_type import SearchCategoryType
from ngl.utils.cache.instrument_cache import InstrumentCache
from rest_framework.views import APIView, Response
from rest_framework.request import Request
from rest_framework import status
from ncl.utils.common.singleton import Singleton

from bzsdp.app.adapter.grpc.deposit.deposit_adapter import DepositAdapter
from bzsdp.app.adapter.grpc.loan.loan_adapter import LoanAdapter
from bzsdp.app.api.serializer.interaction.search.search_symbol_serializer import SearchSerializer
from bzsdp.app.api.serializer.system.visual_item_serializer import VisualItemSerializer
from bzsdp.app.model.vo.interaction.search_vo import SearchVo
from bzsdp.app.logic.interaction.search.search_symbol_logic import SearchSymbolLogic
from bzsdp.app.adapter.grpc.car_price.car_price_adapter import CarAdapter
from ntl.model.bourse.market_enums import MarketType
import re
from operator import itemgetter
from bzsdp.project.config import BZSDPConfig


class SearchSymbolController(APIView):
    target_market_list = {MarketType.BOURSE, MarketType.FARA_BOURSE}

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.logic = SearchSymbolLogic()
        self.car_adapter = CarAdapter()
        self.loan_adapter = LoanAdapter()
        self.deposit_adapter = DepositAdapter()
        self.instrument_cache = InstrumentCache(target_market_list=self.target_market_list,
                                                NGL_CACHE_INFO_REFRESH_INTERVAL_SECOND=60 * 10,
                                                NGL_INSTRUMENT_CACHE_GRPC_URL=BZSDPConfig.NGL_AMALGAM_CACHE_GRPC_URL)

    @lru_cache
    def get(self, request: Request) -> Response:
        serializer = SearchSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        search_query = serializer.data.get(SearchVo.QUERY_STRING)
        page_number = serializer.data.get(SearchVo.PAGE_NUMBER) - 1
        result_list = []
        visual_item_list = self.logic.search_symbol_by_code(search_query)
        for item in visual_item_list:
            added_dict = {}
            added_dict["name"] = item.fa_name
            added_dict['code'] = item.code
            added_dict["company"] = ''
            added_dict["parent"] = item.parent_code
            result_list.append(added_dict)

        car_list_response = self.car_adapter.search_car_by_name(name=search_query)
        for car in car_list_response.car:
            added_dict = {}
            added_dict["name"] = car.name
            added_dict["code"] = car.car_id
            added_dict["company"] = ''
            added_dict["parent"] = SearchCategoryType.BZ_CAR.value

            result_list.append(added_dict)

        loan_list_response = self.loan_adapter.search_loan_by_name(name=search_query)
        for loan in loan_list_response.loan_list:
            added_dict = {}
            added_dict["name"] = loan.name
            added_dict["code"] = loan.loan_id
            added_dict["company"] = ''
            added_dict["parent"] = SearchCategoryType.BZ_LOAN.value

            result_list.append(added_dict)
        bourse_market = self.instrument_cache.find_by_market(
            market_type=MarketType.BOURSE)
        for bourse in list(bourse_market):
            added_dict = {}
            if bourse.persian_name[0:2] != 'ح.' and bourse.persian_name[0:8] != 'اختیارف' and bourse.persian_name[
                                                                                              0:2] != 'ح ':
                if re.findall(pattern=search_query, string=bourse.persian_name) or re.findall(pattern=search_query,
                                                                                              string=bourse.company_persian_name):
                    added_dict["name"] = bourse.persian_name
                    added_dict["code"] = bourse.isin
                    added_dict["company"] = bourse.company_persian_name
                    added_dict["parent"] = SearchCategoryType.BZ_BOURSE.value

                    result_list.append(added_dict)
        fara_bourse_market = self.instrument_cache.find_by_market(
            market_type=MarketType.FARA_BOURSE)
        for fara_bourse in list(fara_bourse_market):
            added_dict = {}
            if fara_bourse.persian_name[0:2] != 'ح.' and fara_bourse.persian_name[
                                                         0:8] != 'اختیارف' and fara_bourse.persian_name[
                                                                               0:2] != 'ح ':
                if re.findall(pattern=search_query, string=fara_bourse.persian_name) or re.findall(pattern=search_query,
                                                                                                   string=fara_bourse.company_persian_name):
                    added_dict["name"] = fara_bourse.persian_name
                    added_dict["code"] = fara_bourse.isin
                    added_dict["company"] = fara_bourse.company_persian_name
                    added_dict["parent"] = SearchCategoryType.BZ_FARA_BOURSE.value

                    result_list.append(added_dict)
        # serializer = VisualItemSerializer(symbol_list, many=True)
        deposit_list = self.deposit_adapter.search_on_deposit(name=search_query)
        for deposit in deposit_list.search_result:
            added_dict = {}
            added_dict["name"] = deposit.name
            added_dict["code"] = deposit.deposit_id
            added_dict["company"] = deposit.company
            added_dict["parent"] = SearchCategoryType.BZ_DEPOSIT.value
            result_list.append(added_dict)

        sorted_lsit = sorted(result_list, key=itemgetter('name'), reverse=False)

        return Response(sorted_lsit[BZSDPConfig.SEARCH_PAGE_NUMBER * page_number:(
                                                                                         page_number + 1) * BZSDPConfig.SEARCH_PAGE_NUMBER],
                        status=status.HTTP_200_OK)
