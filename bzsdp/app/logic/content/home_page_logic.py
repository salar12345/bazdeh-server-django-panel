from typing import Dict

from ncl.utils.common.singleton import Singleton

from bzsdp.app.adapter.grpc.loan.loan_adapter import LoanAdapter
from bzsdp.app.data.dal.content.content_dal import ContentDal
from bzsdp.app.logic.content.home_price_logic import HomePriceLogic

from bzsdp.app.model.dto.home_page.home_page_car import HomePageCar
from bzsdp.app.model.dto.home_page.home_page_crypto_currency import HomePageCryptoCurrency
from bzsdp.app.model.dto.home_page.home_page_currency import HomePageCurrency
from bzsdp.app.model.dto.home_page.home_page_fund import HomePageFund
from bzsdp.app.model.dto.home_page.home_page_home_price import HomePageHomePrice
from bzsdp.app.model.dto.home_page.home_page_instrument import HomePageInstrument
from bzsdp.app.model.dto.home_page.home_page_loan import HomePageLoan
from google.protobuf.json_format import MessageToDict

from bzsdp.project.config import BZSDPConfig


class HomePageLogic(metaclass=Singleton):
    CARIMAGE = "H_CAR.png"
    FUNDIMAGE = "H_FUND.png"
    INSTRUMENTIMAGE = "H_INSTRUMENT.png"
    CURRENCYIMAGE = 'H_CURRENCY.png'
    CRYPTOCURRENCYIMAGE = 'H_CRYPTOCURRENCY.png'
    LOANIMAGE = "H_LOAN.png"
    HOMEPRICEIMAGE = "H_HOME.png"

    def __init__(self):
        super().__init__()
        self.loan_adapter = LoanAdapter()
        self.home_price_logic = HomePriceLogic()
        self.dal = ContentDal()

    def create_home_page_response_model(self, fund, car,
                                        currency_cryptocurrency,
                                        instrument, loan_model, home_price_model):
        result_dict = {}
        car_dict_model = MessageToDict(message=car)
        car_logo = BZSDPConfig.HOME_PAGE_BASE_LOGO_URL + self.CARIMAGE
        car = HomePageCar(logo_url=car_logo,
                          name=car_dict_model.get('singleCar').get('name'),
                          prev_price=None,
                          current_price=car_dict_model.get('singleCar').get('price'),
                          date_time=car_dict_model.get('singleCar').get('date'),
                          category="CAR")

        fund_model = MessageToDict(message=fund)
        fund_logo = BZSDPConfig.HOME_PAGE_BASE_LOGO_URL + self.FUNDIMAGE
        fund = HomePageFund(category="FUND", name=fund_model['fundInfoList'][0]['name'],
                            issuance_price=str(fund_model['fundInfoList'][0]['issuancePrice']),
                            date_time=fund_model['fundInfoList'][0]['lastUpdateDatetime'],
                            logo_url=fund_logo,
                            profit_percent=fund_model['fundInfoList'][0]['lastOneYearProfitPercent'])

        currency_logo = BZSDPConfig.HOME_PAGE_BASE_LOGO_URL + self.CURRENCYIMAGE

        cryptocurrency_logo = BZSDPConfig.HOME_PAGE_BASE_LOGO_URL + self.CRYPTOCURRENCYIMAGE
        first_item = currency_cryptocurrency.pop()
        second_item = currency_cryptocurrency.pop()
        if first_item.uri == "SELL_USD_X_IRR":
            currency = first_item
            crypto = second_item
        else:
            currency = second_item
            crypto = first_item

        if currency.yesterday_closing_price == 0:
            yesterday_price_currency = currency.price
        else:
            yesterday_price_currency = currency.yesterday_closing_price

        currency = HomePageCurrency(category='CURRENCY', name="dollar",
                                    current_price=currency.price, logo_url=currency_logo,
                                    prev_price=yesterday_price_currency,
                                    date_time=currency.datetime_str)

        if crypto.yesterday_closing_price == 0:
            yesterday_price_cryptocurrency = crypto.price
        else:
            yesterday_price_cryptocurrency = crypto.yesterday_closing_price

        crypto_currency = HomePageCryptoCurrency(category='CRYPTO_CURRENCY', name='bitcoin',
                                                 current_price=crypto.price,
                                                 date_time=crypto.datetime_str, logo_url=cryptocurrency_logo,
                                                 prev_price=yesterday_price_cryptocurrency)

        instrument_model = instrument.pop()
        instrument_logo = BZSDPConfig.HOME_PAGE_BASE_LOGO_URL + self.INSTRUMENTIMAGE
        instrument = HomePageInstrument(category="INSTRUMENT",
                                        name=instrument_model.company_persian_name,
                                        current_price=instrument_model.last_traded_price.value,
                                        date_time=str(instrument_model.last_traded_price.last_change_datetime),
                                        prev_price=instrument_model.yesterday_price.value,
                                        logo_url=instrument_logo)

        loan_logo = BZSDPConfig.HOME_PAGE_BASE_LOGO_URL + self.LOANIMAGE
        loan = HomePageLoan(category="LOAN", name=loan_model.loan_type, current_price=str(loan_model.max_loan_integer),
                            date_time=None, logo_url=loan_logo, prev_price=None)

        home_price_logo = BZSDPConfig.HOME_PAGE_BASE_LOGO_URL + self.HOMEPRICEIMAGE
        home_price = HomePageHomePrice(category="HOMEPRICE", name="22",
                                       current_price=str(home_price_model["last_price"]),
                                       month=home_price_model["month"], year=home_price_model["year"],
                                       logo_url=home_price_logo,
                                       prev_price=str(home_price_model["prev_price"]))

        return [currency, loan, crypto_currency, car, home_price, instrument, fund]

    def cache_home_page_result(self, home_page: Dict):
        self.dal.cache_home_page(home_page=home_page)

    def get_home_page(self):
        return self.dal.get_home_page()
