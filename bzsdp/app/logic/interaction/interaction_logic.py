from typing import List, Dict, Optional

from bzscl.model.entity.member.member_entity import MemberEntity

from ncl.utils.common.singleton import Singleton

from ntl.model.amalgam.priceable_enums import AFRAEcoPriceableType
from rest_framework.utils.serializer_helpers import ReturnDict
from bzsdp.app.api.serializer.interaction.gold_calculator_serializer import GoldCalculatorSerializer
from bzsdp.app.data.dal.interaction.interaction_dal import InteractionDal
from bzsdp.app.model.vo.interaction.interaction_vo import InteractionVO
from bzsdp.app.model.vo.interaction.news_analysis_like_vo import NewsAnalysisLikeVO


class InteractionLogic(metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.dal = InteractionDal()
        self.bahar_and_emami_coin_weight = 8.133
        self.half_coin = 4.066
        self.quarter_coin = 2.032
        self.one_gr_coin = 1
        self.constant_value_denominator = 31.1
        self.constant_value_numerator = 0.9

    def get_active_vote(self) -> bool:
        if self.dal.get_active_vote():
            return True
        else:
            return False

    def get_member_participate(self, gps_adid: Optional[str] = None) -> bool:
        if gps_adid is not None:
            result = self.dal.get_member_participate(gps_adid=gps_adid)
            if result:
                return True
            else:
                return False
        else:
            return False

    def save_report(self, news_url: str) -> bool:

        return self.dal.save_report(news_url=news_url)

    def save_reported_message(self, message: ReturnDict, member: MemberEntity) -> bool:

        return self.dal.save_message(message=message, member=member)

    def determine_coin_weight(self, target_uri: str = None):
        if target_uri == AFRAEcoPriceableType.PC_GOLD_COIN_BAHAR.db_value or \
                target_uri == AFRAEcoPriceableType.PC_GOLD_COIN_EMAMI.db_value:
            return self.bahar_and_emami_coin_weight

        elif target_uri == AFRAEcoPriceableType.PC_GOLD_COIN_HALF.db_value:
            return self.half_coin

        elif target_uri == AFRAEcoPriceableType.PC_GOLD_COIN_QUARTER.db_value:
            return self.quarter_coin

        elif target_uri == AFRAEcoPriceableType.PC_GOLD_COIN_ONE_GRAM.db_value:
            return self.one_gr_coin
        else:
            return None

    def calculate_gold_bubble(self, gold_ounce_price: int = None, dollar_price: int = None,
                              right_to_mint_coin: int = None, coin_weight: int = None, coin_price: int = None):

        gold_inherent = ((
                                 coin_weight * self.constant_value_numerator * gold_ounce_price * dollar_price) / self.constant_value_denominator) + right_to_mint_coin

        gold_bubble = coin_price - gold_inherent

        return gold_inherent, gold_bubble

    def calculate_gold_calculator(self, serialized_data: GoldCalculatorSerializer):
        tax = serialized_data.data[InteractionVO.TAX] / 100
        benefit = serialized_data.data[InteractionVO.BENEFIT]
        benefit = benefit / 100
        if serialized_data.data[InteractionVO.WAGE_TYPE] == "RIAL":
            base_price = (serialized_data.data[InteractionVO.WAGE] + serialized_data.data[InteractionVO.PRICE]) * \
                         serialized_data.data[InteractionVO.WEIGHT]
            result = base_price + base_price * (tax + benefit)
        elif serialized_data.data[InteractionVO.WAGE_TYPE] == "PERCENT":
            wage = serialized_data.data[InteractionVO.WAGE] / 100
            wage_percent = wage * serialized_data.data[InteractionVO.PRICE]
            base_price = (wage_percent + serialized_data.data[InteractionVO.PRICE]) * serialized_data.data[
                InteractionVO.WEIGHT]
            result = base_price + base_price * (tax + benefit)
        else:
            return None

        return result

    def add_news_bookmark(self, member: MemberEntity, news_id: str) -> bool:
        return self.dal.save_news_bookmark(member=member, news_id=news_id)

    def get_bookmark_id_list(self, member: MemberEntity) -> List[Dict]:
        return self.dal.get_news_bookmark_id_list(member=member)

    def delete_news_bookmark(self, member: MemberEntity, news_id: str) -> bool:
        return self.dal.delete_news_bookmark(member=member, news_id=news_id)

    # watchlist
    def get_all_watchlist_entity(self, member: MemberEntity):
        return self.dal.get_all_watchlist_entity(member=member)

    def save_code_to_watchlist_in_watchlist_entity(self, code: str, parent_code: str, member: MemberEntity):

        self.dal.save_code_to_watchlist(code=code, member=member, parent_code=parent_code)

    def delete_item_from_watchlist_entity(self, member: MemberEntity, one_item_in_watchlist_code: str):

        self.dal.delete_item_from_watchlist(member=member,
                                            one_item_in_watchlist_code=one_item_in_watchlist_code)

    # vote

    def get_vote(self):
        question, question_id, multiple = self.dal.get_vote()
        if question_id:
            choice_question_list, choice_id_list = self.dal.get_choices(id=question_id)

            return question, question_id, multiple, choice_question_list, choice_id_list
        else:
            return None, None, False, [], []

    def submit_vote(self, question_id: str = "", choices_id_list: list = [], dismiss: bool = False,
                    is_member: bool = False):

        self.dal.submit_vote(question_id=question_id, dismiss=dismiss, is_member=is_member)

        for choice in choices_id_list:
            self.dal.submit_vote_and_choices(choices_id=choice)

    def save_user_vote(self, gps_adid, question_id):
        self.dal.save_user_vote(gps_adid=gps_adid, question_id=question_id)

    # news_analysis

    def do_like(self, news_analysis_id, member: MemberEntity, state, news_or_analysis):
        if news_or_analysis == NewsAnalysisLikeVO.NEWS:
            self.dal.do_like(news_id=news_analysis_id, analysis_id=None, member=member, state=state)
        elif news_or_analysis == NewsAnalysisLikeVO.ANALYSIS:
            self.dal.do_like(news_id=None, analysis_id=news_analysis_id, member=member, state=state)

    def do_dislike(self, news_analysis_id, member: MemberEntity, state, news_or_analysis):
        if news_or_analysis == NewsAnalysisLikeVO.NEWS:
            self.dal.do_dislike(news_id=news_analysis_id, analysis_id=None, member=member, state=state)
        elif news_or_analysis == NewsAnalysisLikeVO.ANALYSIS:
            self.dal.do_dislike(news_id=None, analysis_id=news_analysis_id, member=member, state=state)

    def add_news_or_analysis_to_has_been_read_entity(self, member: MemberEntity, news_or_analysis, news_or_analysis_id):
        if news_or_analysis == InteractionVO.NEWS:
            self.dal.add_news_or_analysis_to_has_been_read_entity(member=member, news_id=news_or_analysis_id,
                                                                  analysis_id=None)
        elif news_or_analysis == InteractionVO.ANALYSIS:
            self.dal.add_news_or_analysis_to_has_been_read_entity(member=member, news_id=None,
                                                                  analysis_id=news_or_analysis_id)

    def create_news_analysis_like_data_model(self, member: MemberEntity, news_analysis_id, news_or_analysis):
        news_id = analysis_id = None
        if news_or_analysis == NewsAnalysisLikeVO.NEWS:
            news_id = news_analysis_id
        elif news_or_analysis == NewsAnalysisLikeVO.ANALYSIS:
            analysis_id = news_analysis_id
        response_dict = {}
        response_dict[InteractionVO.LIKE_STATE] = self.dal.get_news_analysis_like_member_state(member=member,
                                                                                               news_id=news_id,
                                                                                               analysis_id=analysis_id)
        response_dict[InteractionVO.DISLIKE_STATE] = self.dal.get_news_analysis_dislike_member_state(member=member,
                                                                                                     news_id=news_id,
                                                                                                     analysis_id=analysis_id)
        response_dict[InteractionVO.LIKE_COUNT], response_dict[
            InteractionVO.DISLIKE_COUNT] = self.dal.get_news_analysis_like_dislike_count(news_id=news_id,
                                                                                         analysis_id=analysis_id)
        return response_dict
