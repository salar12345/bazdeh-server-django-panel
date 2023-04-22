import json

from ncl.utils.common.singleton import Singleton
from ngl.utils.cache.amalgam_cache import AmalgamCache
from ngl.utils.cache.instrument_cache import InstrumentCache

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from bzsdp.app.adapter.grpc.car_price.car_price_adapter import CarAdapter

from bzsdp.app.adapter.grpc.cryptocurrency_currency_fund_price.cryptocurrency_currency_price import \
    CurrencyCryptoCurrencyFundPriceAdapter
from bzsdp.app.adapter.grpc.instrument_price.instrument_price import InstrumentPriceAdapter
from bzsdp.app.adapter.grpc.loan.loan_adapter import LoanAdapter
from bzsdp.app.api.controller.base_api_view import BasePanelController
from bzsdp.app.logic.content.home_page_logic import HomePageLogic
from bzsdp.app.logic.content.home_price_logic import HomePriceLogic

from bzsdp.project.config import BZSDPConfig

class HomePageController(BasePanelController, APIView, metaclass=Singleton):
    def __init__(self):
        super().__init__()

        self.car_price_adapter = CarAdapter()
        self.cc_fund_price_adapter = CurrencyCryptoCurrencyFundPriceAdapter()
        self.logic = HomePageLogic()
        self.loan_adapter = LoanAdapter()
        self.home_price_logic = HomePriceLogic()
        self.amalgam_cache = AmalgamCache()
        self.instrument_cache = InstrumentCache(NGL_INSTRUMENT_CACHE_GRPC_URL=BZSDPConfig.GRPC_SERVE_HOST_AFRA,
                                                target_instrument_isin_list=BZSDPConfig.HOME_PAGE_INSTRUMENT_ISIN_CODE,
                                                NGL_CACHE_INFO_REFRESH_INTERVAL_SECOND=BZSDPConfig.REFRESH_INTERVAL_SECOND,
                                                HAS_MOST_TRADE_VALUE=True, HAS_MOST_TRADE_VOLUME=True,
                                                HAS_MOST_PRICE_PERCENT_CHANGES=True,
                                                HAS_MOST_MARKET_VALUE=True,
                                                HAS_MOST_INDEX_EFFECT=True,
                                                HAS_MOST_TRADED_PRICE=True)

    def get(self, request):
        # todo change to read from RDB

        cache_model = self.logic.get_home_page()
        if cache_model:
            result = cache_model

        else:
            car_price = self.car_price_adapter.get_single_car(name="پژو 206", model="تیپ 2", production_year=1401)
            fund_price = self.cc_fund_price_adapter.get_fund_info(fund_code=[BZSDPConfig.HOME_PAGE_FUND_CODE])
            currency_cryptocurrency_price = self.amalgam_cache.find_by_uris(
                set(BZSDPConfig.HOME_PAGE_CURRENCY_CRYPTOCURRENCY_CODE))
            instrment_info = self.instrument_cache.find_by_isins(
                isin_set=set(BZSDPConfig.HOME_PAGE_INSTRUMENT_ISIN_CODE))
            loan_model = self.loan_adapter.get_single_loan(loan_id=BZSDPConfig.HOME_PAGE_LOAN_CODE).single_loan
            home_price_model = self.home_price_logic.last_home_price_average_price()

            response_model = self.logic.create_home_page_response_model(fund=fund_price, car=car_price,
                                                                        currency_cryptocurrency=currency_cryptocurrency_price,
                                                                        instrument=instrment_info,
                                                                        loan_model=loan_model,
                                                                        home_price_model=home_price_model)

            response = [json.dumps(x.__dict__) for x in response_model]
            response_dict = [json.loads(x) for x in response]
            result = {}
            result["result"] = response_dict
            self.logic.cache_home_page_result(home_page=result)
            result = self.logic.get_home_page()

        return Response(json.loads(result), status=status.HTTP_200_OK)
