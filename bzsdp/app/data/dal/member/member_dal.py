import uuid
from builtins import tuple
from datetime import datetime

from bzscl.model.entity.member.device_entity import DeviceEntity
from bzscl.model.entity.member.member_entity import MemberEntity
from bzscl.model.entity.member.portfolio_entity import PortfolioEntity
from ncl.utils.common.singleton import Singleton

from bzsdp.app.data.dao.member.member_dao import MemberDao
from bzsdp.app.data.rd_dao.member.member_rd_dao import MemberRdDao


class MemberDal(metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.rddao = MemberRdDao()
        self.dao = MemberDao()

    def cache_member_login_info(self, code: int, noence: str, phone_number: str) -> bool:
        self.rddao.save_sms_code(code=code, noence=noence, phone_number=phone_number)

    def find_member_by_phone_number(self, phone_number: str) -> MemberEntity:
        member = self.dao.find_member_by_phone_number(phone_number=phone_number)
        return member

    def get_code_and_phone_number(self, noence: str) -> tuple:
        code, phone_number = self.rddao.get_sms_code(noence=noence)
        return code, phone_number

    def register_member(self, phone_number: str, user_tag: str):
        return self.dao.register_member(phone_number=phone_number, user_tag=user_tag)

    def get_portfolios(self, member: MemberEntity):
        return self.dao.get_portfolios(member=member)

    def add_portfolio(self, member: MemberEntity, name: str):
        return self.dao.add_portfolio(member=member,
                                      name=name)

    def get_asset_count(self, portfolio: PortfolioEntity):
        return self.dao.get_asset_count(portfolio=portfolio)

    def delete_portfolio(self, portfolio_id: uuid):
        return self.dao.delete_portfolio(portfolio_id=portfolio_id)

    def get_all_assets(self, member: MemberEntity):
        return self.dao.get_all_assets(member=member)

    def get_assets_by_portfolio(self, member: MemberEntity, portfolio_id: uuid):
        return self.dao.get_assets_by_portfolio(member=member, portfolio_id=portfolio_id)

    def save_details_of_asset(self, member: MemberEntity, name: str, code: str, parent_code: str,
                              company_name: str, portfolio_id: uuid, count: float, buy_price: float, base_value: float,
                              date_time: datetime, description: str, daily_usd_price: float):
        return self.dao.save_details_of_asset(member=member, name=name, code=code, parent_code=parent_code,
                                              portfolio_id=portfolio_id, company_name=company_name, count=count,
                                              buy_price=buy_price, date_time=date_time, description=description,
                                              daily_usd_price=daily_usd_price, base_value=base_value)

    def update_asset(self, asset_id: uuid, name: str, code: str,
                     count: float, buy_price: float, date_time: datetime,
                     description: str, daily_usd_price: float):
        return self.dao.update_asset(
            asset_id=asset_id, name=name, code=code, count=count, buy_price=buy_price,
            date_time=date_time, description=description,
            daily_usd_price=daily_usd_price
        )

    def get_asset_by_id(self, asset_id: uuid):
        return self.dao.get_asset_by_id(asset_id=asset_id)

    def delete_asset(self, asset_id: uuid):
        return self.dao.delete_asset(asset_id=asset_id)

    def delete_member_jwt_token(self, member: MemberEntity):
        return self.dao.delete_member_jwt_token(member=member)

    def get_user_searches(self, member_id: uuid):
        return self.rddao.get_user_searches(member_id=member_id)

    def save_user_search(self, member_id: str, search_word: str):
        if len(search_word) >= 3:
            self.rddao.save_user_search(member_id=member_id, search_word=search_word)

    def get_profile_by_member(self, member: MemberEntity):
        return self.dao.get_profile_by_member(member=member)

    def edit_profile(self, member: MemberEntity, name: str, last_name: str, image_url: str):
        return self.dao.edit_profile(member=member, name=name, last_name=last_name, image_url=image_url)


    def get_member_by_id(self, member_id: str) -> MemberEntity:
        return self.dao.get_by_id(member_id)

    def update_phone_number(self, member: MemberEntity, phone_number: str):
        self.dao.update_phone_number(member=member, phone_number=phone_number)

    def create_member_device_relation(self,member:MemberEntity, device:DeviceEntity):
        self.dao.create_member_device_relation(member=member, device=device)

    def exist_tag(self, tag):
        return self.dao.exist_tag(tag)

