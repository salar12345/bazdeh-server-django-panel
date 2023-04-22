import logging


from bzscl.model.enum.content.news_general_category_type import NewsGeneralCategoryGroupType
from ncl.utils.helper.commons_utils import CommonsUtils
from ntl.model.amalgam.priceable_enums import AFRAEcoPriceableType
from ntl.model.nlp.topic_enums import AFRAEcoTopicType


from sentry_sdk import capture_exception
import traceback
from marshmallow import ValidationError

from bzsdp.project.config import BZSDPConfig


class Utils(CommonsUtils):

    @staticmethod
    def handle_exception(e):
        if BZSDPConfig.ENABLE_SENTRY:
            logging.info(e)
            capture_exception(e)
        else:
            print(f'exception={e}, traceback={traceback.print_exc()}')
        print(e)

    @staticmethod
    def handle_validation_error(err):
        if BZSDPConfig.ENABLE_SENTRY:
            ValidationError.normalized_messages(err)
        else:
            print(f'exception={err}, traceback={traceback.print_exc()}')
        print(err)

    @classmethod
    def standardize_string_datetime(cls, date_string: str) -> str:
        datetime_ = cls.get_datetime_from_string_datetime(date_string)
        return cls.get_string_datetime_from_datetime(datetime_)

    @classmethod
    def get_string_datetime_from_datetime(cls, d, format_: str = None) -> str:
        if format_ is None:
            format_ = "%Y-%m-%dT%H:%M:%S.%f"
        return d.strftime(format_)

    @staticmethod
    def change_input_topic_and_pirceables(target_uris,category_types):
        eco_topic_in = list()
        priceables_in = list()

        try:

            if target_uris:
                priceables_in = [target_uri for target_uri in target_uris if
                                 AFRAEcoPriceableType.find_by_value(target_uri)]
                if not priceables_in:
                    priceables_in = target_uris

            if category_types:
                for category_type in category_types:

                    if category_type == NewsGeneralCategoryGroupType.BZ_BOURSE.value or category_type == NewsGeneralCategoryGroupType.BZ_CRYPTOCURRENCY.value or category_type == NewsGeneralCategoryGroupType.BZ_CURRENCY.value or category_type == NewsGeneralCategoryGroupType.BZ_INVESTMENTFUND.value:
                        eco_topic_in.append(category_type.replace("BZ", "E"))

                    if category_type == NewsGeneralCategoryGroupType.BZ_GOLDCOIN.value:
                        eco_topic_in.append(AFRAEcoTopicType.E_PRECIOUSMETALSANDCOINS.db_value)
                        priceables_in.append(AFRAEcoPriceableType.PC_GOLD_COIN_BAHAR.db_value)
                        priceables_in.append(AFRAEcoPriceableType.PC_GOLD_COIN_EMAMI.db_value)
                        priceables_in.append(AFRAEcoPriceableType.PC_GOLD_COIN_QUARTER.db_value)
                        priceables_in.append(AFRAEcoPriceableType.PC_GOLD_COIN_ONE_GRAM.db_value)
                        priceables_in.append(AFRAEcoPriceableType.PC_GOLD_COIN_HALF.db_value)

                    if category_type == NewsGeneralCategoryGroupType.BZ_GOLDANDVALUABLEMETALS.value:
                        eco_topic_in.append(AFRAEcoTopicType.E_PRECIOUSMETALSANDCOINS.db_value)
                        priceables_in.append(AFRAEcoPriceableType.PC_GOLD_GRAM_24.db_value)
                        priceables_in.append(AFRAEcoPriceableType.PC_GOLD_MITHQAL.db_value)
                        priceables_in.append(AFRAEcoPriceableType.PC_GOLD_OUNCE.db_value)
                        priceables_in.append(AFRAEcoPriceableType.PC_GOLD_GRAM_18.db_value)
                        priceables_in.append(AFRAEcoPriceableType.PC_SILVER_OUNCE.db_value)
                        priceables_in.append(AFRAEcoPriceableType.PC_PLATINUM_OUNCE.db_value)

                    if category_type == NewsGeneralCategoryGroupType.BZ_INDUSTRY.value:
                        for industry_ecotopic in AFRAEcoTopicType:
                            if industry_ecotopic.parent is None and industry_ecotopic.grand_parent is None:
                                continue
                            else:
                                eco_topic_in.append(industry_ecotopic.db_value)

        except Exception as execption:
            logging.info(execption)

        return eco_topic_in,priceables_in



