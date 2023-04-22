import uuid
import datetime

from bzscl.model.entity.member.device_entity import DeviceEntity
from bzscl.model.entity.member.member_entity import MemberEntity
from bzscl.model.entity.member.portfolio_entity import PortfolioEntity
from ncl.utils.common.singleton import Singleton
from rest_framework_simplejwt.tokens import RefreshToken

from bzsdp.app.data.dal.interaction.interaction_dal import InteractionDal
from bzsdp.app.data.dal.member.member_dal import MemberDal
import random
import string

from bzsdp.app.model.vo.member.profile_vo import ProfileVO
from bzsdp.app.data.dal.interaction.risk_measurement_vote_dal import RiskMeasurementVoteDal


class MemberLogic(metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.dal = MemberDal()
        self.interaction_dal = InteractionDal()
        self.risk_measurement_vote_dal = RiskMeasurementVoteDal()

    def cache_code_and_noence(self, code: int, noence: str, phone_number: str) -> bool:
        self.dal.cache_member_login_info(code=code, noence=noence, phone_number=phone_number)

    def create_code_and_noence(self):
        code = random.randint(1000, 9999)
        noence = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
        return code, noence

    def find_member_by_phone_number(self, phone_number: str) -> MemberEntity:
        member = self.dal.find_member_by_phone_number(phone_number=phone_number)
        return member

    def get_code_and_phone_number(self, noence: str) -> tuple:
        code, phone_number = self.dal.get_code_and_phone_number(noence=noence)
        return code, phone_number

    def register_member(self, phone_number: str):
        user_tag = self.get_random_string(4)
        if not user_tag:
            user_tag = self.get_random_string(4)
        if self.dal.exist_tag(user_tag):
            user_tag = self.get_random_string(4)

        return self.dal.register_member(phone_number=phone_number, user_tag=user_tag)



    def get_random_string(self, length):
        letters = string.ascii_uppercase + "1234567890"
        result_str = ''.join(random.choice(letters) for i in range(length))
        return result_str

    def generate_member_token(self, member: MemberEntity):
        refresh_token = RefreshToken.for_user(user=member)
        access_token = refresh_token.access_token
        return refresh_token, access_token

    def generate_access_token(self, refresh_token: str):
        refresh_token = RefreshToken(refresh_token)
        return refresh_token.access_token

    def get_portfolios(self, member: MemberEntity):
        return self.dal.get_portfolios(member=member)

    def add_portfolio_for_member(self, member: MemberEntity, name: str):
        return self.dal.add_portfolio(member=member,
                                      name=name)

    def get_count_of_assets(self, portfolio: PortfolioEntity):
        return self.dal.get_asset_count(portfolio=portfolio)

    def delete_portfolio(self, portfolio_id: uuid):
        return self.dal.delete_portfolio(portfolio_id=portfolio_id)

    def get_all_assets(self, member: MemberEntity):
        return self.dal.get_all_assets(member=member)

    def get_assets_by_portfolio(self, member: MemberEntity, portfolio_id: uuid):
        return self.dal.get_assets_by_portfolio(member=member, portfolio_id=portfolio_id)

    def save_details_of_asset(self, member: MemberEntity, name: str, code: str, parent_code: str,
                              company_name: str, portfolio_id: uuid, count: float, buy_price: float, base_value: float,
                              date_time: datetime, description: str, daily_usd_price: float):
        return self.dal.save_details_of_asset(member=member, name=name, code=code, parent_code=parent_code,
                                              portfolio_id=portfolio_id, company_name=company_name, count=count,
                                              buy_price=buy_price, date_time=date_time, description=description,
                                              daily_usd_price=daily_usd_price, base_value=base_value)

    def get_asset_by_id(self, asset_id: uuid):
        return self.dal.get_asset_by_id(asset_id=asset_id)

    def update_asset(self, asset_id: uuid, name: str, code: str,
                     count: float, buy_price: float, date_time: datetime,
                     description: str, daily_usd_price: float):
        return self.dal.update_asset(asset_id=asset_id, name=name, code=code, count=count, buy_price=buy_price,
                                     date_time=date_time, description=description,
                                     daily_usd_price=daily_usd_price)

    def delete_asset(self, asset_id: uuid):
        return self.dal.delete_asset(asset_id=asset_id)

    def delete_member_jwt_token(self, member: MemberEntity):
        return self.dal.delete_member_jwt_token(member=member)

    def get_user_searches(self, member_id: uuid):
        return self.dal.get_user_searches(member_id=member_id)

    def save_user_search(self, member_id: str, search_word: str):
        if len(search_word) >= 3:
            self.dal.save_user_search(member_id=member_id, search_word=search_word)

    def check_if_user_is_logged_in(self, member: MemberEntity) -> bool:
        return True if member.phone_number else False

    def get_profile_by_member(self, member: MemberEntity):
        profile = self.dal.get_profile_by_member(member=member)
        (
            profile.news_has_been_read_count,
            profile.analysis_has_been_read_count
        ) = self.interaction_dal.get_count_of_has_been_read_news_and_analysis(member=member)
        profile.risk_measurement_attendance = self.risk_measurement_vote_dal.exists(
            self.risk_measurement_vote_dal.filter(member=member)
        )
        if profile.risk_measurement_attendance:
            profile.risk_measurement_score = sum(
                self.risk_measurement_vote_dal.values_list(
                    'choice__score',
                    qs=self.risk_measurement_vote_dal.filter(member=member),
                    flat=True
                )
            )
        return profile

    def edit_profile(self, member: MemberEntity, name: str, last_name: str, image_url: str):
        return self.dal.edit_profile(member=member, name=name, last_name=last_name, image_url=image_url)


    def get_profile_images(self):
        profile_images = [
            ProfileVO.DEADMAN,
            ProfileVO.GOODBOY,
            ProfileVO.GLASSBOY,
            ProfileVO.HAPPYGIRL,
            ProfileVO.NERDBOY,
            ProfileVO.OLDFASHIONGIRL
        ]
        return profile_images

    def get_member_by_id(self, member_id: str) -> MemberEntity:
        return self.dal.get_member_by_id(member_id)

    def update_phone_number(self, member:MemberEntity, phone_number:str):
        self.dal.update_phone_number(member=member, phone_number=phone_number)

    def create_member_device_relation(self, member:MemberEntity, device:DeviceEntity):
        self.dal.create_member_device_relation(member=member, device=device)


