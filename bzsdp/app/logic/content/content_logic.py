import datetime
from ncl.utils.common.singleton import Singleton
from datetime import datetime
from bzsdp.app.model.vo.content.car_price_vo import CarPriceVO
from bzsdp.app.model.vo.content.loan_vo import LoanVO
from ntl.model.amalgam.car_type_enums import CarTypeEnums
from bzsdp.app.utils.grpc.grpc_utils import GrpcUtils
from bzsdp.project.config import BZSDPConfig
from bzsdp.utils.utils import Utils


class ContentLogic(metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.grpc_utils = GrpcUtils()

    @classmethod
    def calculate_installment(cls, loan_amount: float = 0, profit: float = 0, num_of_installment: int = 0):
        installment_value = int((loan_amount * (profit / 1200) * ((1 + (profit / 1200)) ** num_of_installment)) / (
                ((1 + (profit / 1200)) ** num_of_installment) - 1))
        return installment_value

    def serve_related_loans_dictionary(self, grpc_repited_response):
        list_of_grpc_response = grpc_repited_response.related_loan
        total_loan = list()
        total_loan.extend(list_of_grpc_response)
        loan_dict_list = []
        for proto_loan in total_loan:
            loan_dict = {}
            loan_dict[LoanVO.LOAN_ID] = proto_loan.loan_id
            loan_dict[LoanVO.IMAGE] = proto_loan.image
            loan_dict[LoanVO.NAME] = proto_loan.name
            loan_dict[LoanVO.INTEREST_REVENUE] = proto_loan.interest_revenue
            loan_dict[LoanVO.TYPE_OF_GUARANTEE] = proto_loan.type_of_guarantee
            loan_dict[LoanVO.MAX_LOAN] = proto_loan.max_loan
            loan_dict[LoanVO.MAXIMUM_PAYMENT_TIME] = proto_loan.maximum_payment_time
            loan_dict_list.append(loan_dict)
        return loan_dict_list

    def serve_loan_list_dictionary(self, grpc_repited_response):
        list_of_grpc_response = grpc_repited_response.loan_list
        total_loan = list()
        total_loan.extend(list_of_grpc_response)
        loan_dict_list = []
        for proto_loan in total_loan:
            loan_dict = {}
            loan_dict[LoanVO.NAME] = proto_loan.name
            loan_dict[LoanVO.MAXIMUM_PAYMENT_TIME] = proto_loan.maximum_payment_time
            loan_dict[LoanVO.INTEREST_REVENUE] = proto_loan.interest_revenue
            loan_dict[LoanVO.TYPE_OF_GUARANTEE] = proto_loan.type_of_guarantee
            loan_dict[LoanVO.MAX_LOAN] = proto_loan.max_loan
            loan_dict[LoanVO.LOAN_TYPE] = proto_loan.loan_type
            loan_dict[LoanVO.LOAN_ID] = proto_loan.loan_id
            loan_dict[LoanVO.LOAN_TYPE_ID] = proto_loan.loan_type_id
            loan_dict[LoanVO.IMAGE] = proto_loan.image
            loan_dict_list.append(loan_dict)
        return loan_dict_list

    def serve_single_loan_dictionary(self, proto_single_loan):
        proto_loan = proto_single_loan.single_loan
        loan_dict = {}
        loan_dict[LoanVO.NAME] = proto_loan.name
        loan_dict[LoanVO.COMPANY] = proto_loan.company
        loan_dict[LoanVO.LOAN_NAME] = proto_loan.loan_name
        loan_dict[LoanVO.INTEREST_REVENUE] = proto_loan.interest_revenue
        loan_dict[LoanVO.MAX_LOAN] = proto_loan.max_loan
        loan_dict[LoanVO.LOAN_MIN] = proto_loan.loan_min
        loan_dict[LoanVO.TYPE_OF_GUARANTEE] = proto_loan.type_of_guarantee
        loan_dict[LoanVO.BLOCKED_DEPOSIT] = proto_loan.blocked_deposit
        loan_dict[LoanVO.BLOCKED_DEPOSIT_BOOLIAN] = proto_loan.blocked_deposit_boolian
        loan_dict[LoanVO.DEPOSIT_TIME_LIMIT] = proto_loan.deposit_time_limit
        loan_dict[LoanVO.DEPOSIT_REQUIRED] = proto_loan.deposit_required
        loan_dict[LoanVO.REQUIRES_DEPOSIT_BOOLIAN] = proto_loan.requires_deposit_boolian
        loan_dict[LoanVO.DEPOSIT_ACCOUNT] = proto_loan.deposit_account
        loan_dict[LoanVO.DEPOSIT_VALUE] = proto_loan.deposit_value
        loan_dict[LoanVO.DEPOSIT_PROFIT] = proto_loan.deposit_profit
        loan_dict[LoanVO.DEPOSIT_SLEEP_DURATION] = proto_loan.deposit_sleep_duration
        loan_dict[LoanVO.RATIO_LOAN_TO_DEPOSIT] = proto_loan.ratio_loan_to_deposit
        loan_dict[LoanVO.MAXIMUM_PAYMENT_TIME] = proto_loan.maximum_payment_time
        loan_dict[LoanVO.LOAN_INSTALLMENT] = proto_loan.loan_Installment
        loan_dict[LoanVO.TOTAL_PROFIT] = proto_loan.total_profit
        loan_dict[LoanVO.TOTAL_LOAN_PROFIT] = proto_loan.total_loan_profit
        loan_dict[LoanVO.SEPARATE_DEPOSIT] = proto_loan.separate_deposit
        loan_dict[LoanVO.OTHER_COSTS] = proto_loan.other_costs
        loan_dict[LoanVO.CONDITIONS] = proto_loan.conditions
        loan_dict[LoanVO.OPPORTUNITY_COST_BLOCKED] = proto_loan.opportunity_cost_blocked
        loan_dict[LoanVO.IMAGE] = proto_loan.image
        loan_dict[LoanVO.SINGLE_URL] = proto_loan.single_url
        loan_dict[LoanVO.RADE_LAST_UPDATE_DATETIME] = proto_loan.rade_last_update_datetime
        loan_dict[LoanVO.PROFIT_INTEGER] = proto_loan.profit_integer
        loan_dict[LoanVO.MAX_LOAN_INTEGER] = proto_loan.max_loan_integer
        loan_dict[LoanVO.MAXIMUM_PAYMENT_TIME_INTEGER] = proto_loan.maximum_payment_time_integer
        loan_dict[LoanVO.IS_ACTIVE] = proto_loan.is_active
        loan_dict[LoanVO.LOAN_TYPE] = proto_loan.loan_type
        loan_dict[LoanVO.LOAN_TYPE_ID] = proto_loan.loan_type_id
        loan_dict[LoanVO.LAST_UPDATE_DATETIME] = proto_loan.last_update_datetime
        loan_dict[LoanVO.LOAN_ID] = proto_loan.loan_id
        return loan_dict

    def create_car_last_price_model(self, cars_price: list = None):
        car_list = []

        for car_price in cars_price:
            dict_car_type = {}

            dict_car_type[CarPriceVO.TARGET_URI] = car_price.basic_info.car_entity_name
            dict_car_type[CarPriceVO.CAR_TYPE_FA_NAME] = car_price.basic_info.fa_name
            dict_car_type[CarPriceVO.PRICE] = car_price.price_point.PRICE
            dict_car_type[CarPriceVO.DATE] = car_price.price_point.DATE
            dict_car_type[CarPriceVO.PRODUCTION_YEAR] = car_price.price_point.production_year
            price_type = self.grpc_utils.transfer_afra_car_price_type_to_string(
                car_price_type=car_price.price_point.price_type)
            dict_car_type[CarPriceVO.PRICE_TYPE] = price_type

            car_type_enum = CarTypeEnums.find_by_value(db_value=car_price.basic_info.car_entity_name)
            dict_car_type[CarPriceVO.ATTRIBUTE] = car_type_enum.attribute

            car_model = car_type_enum.model
            car_model_db_value = car_model.db_value
            car_model_fa_name = car_model.fa_name
            dict_car_type[CarPriceVO.MODEL_DB_VALUE] = car_model_db_value
            dict_car_type[CarPriceVO.MODEL_FA_NAME] = car_model_fa_name

            car_brand = car_model.brand
            car_brand_db_value = car_brand.db_value
            car_brand_fa_name = car_brand.fa_name
            dict_car_type[CarPriceVO.BRAND_DB_VALUE] = car_brand_db_value
            dict_car_type[CarPriceVO.BRAND_FA_NAME] = car_brand_fa_name

            car_company_name = car_brand.company_name
            car_company_db_value = car_company_name.db_value
            car_company_fa_name = car_company_name.fa_name
            dict_car_type[CarPriceVO.COMPANY_DB_VALUE] = car_company_db_value
            dict_car_type[CarPriceVO.COMPANY_FA_NAME] = car_company_fa_name

            car_list.append(dict_car_type)

        return car_list

    def create_historical_price_start_dateime_and_end_datetime(self):
        end_date_time = datetime.datetime.now()
        start_date_time = end_date_time - datetime.timedelta(months=BZSDPConfig.CARTIMEDELTA)

        str_end_date_time = str(end_date_time).split(" ")[0]
        str_start_date_time = str(start_date_time).split(" ")[0]

        return str_start_date_time, str_end_date_time

    def create_car_historical_price_model(self, chart_points: list = None):
        point_list = []

        for point in chart_points:
            point_dict = {}
            point_dict[CarPriceVO.PRICE] = point[0].PRICE
            point_dict[CarPriceVO.DATE] = point[0].DATE
            point_list.append(point_dict)

        return point_list

    def serve_car_list_dictionary(self, grpc_repeated_response):
        list_of_grpc_response = grpc_repeated_response.car
        total_cars = list()
        total_cars.extend(list_of_grpc_response)
        car_dict_list = []
        for proto_car in total_cars:
            car_dict = {}
            car_dict[CarPriceVO.CAR_ID] = proto_car.car_id
            car_dict[CarPriceVO.TARGET_URI] = ""
            car_dict[CarPriceVO.CAR_TYPE_FA_NAME] = ""
            car_dict[CarPriceVO.PRICE] = proto_car.price
            car_dict[CarPriceVO.DATE] = proto_car.date[:10]
            car_dict[CarPriceVO.PRODUCTION_YEAR] = proto_car.production_year
            car_dict[CarPriceVO.ATTRIBUTE] = proto_car.model
            car_dict[CarPriceVO.PRICE_TYPE] = CarPriceVO.BAZAAR
            car_dict[CarPriceVO.MODEL_DB_VALUE] = proto_car.name
            car_dict[CarPriceVO.MODEL_FA_NAME] = proto_car.name
            car_dict[CarPriceVO.BRAND_DB_VALUE] = proto_car.brand_fa_name
            car_dict[CarPriceVO.BRAND_FA_NAME] = proto_car.brand_fa_name
            car_dict[CarPriceVO.COMPANY_DB_VALUE] = proto_car.brand_fa_name
            car_dict[CarPriceVO.COMPANY_FA_NAME] = proto_car.brand_fa_name
            car_dict_list.append(car_dict)
        return car_dict_list
