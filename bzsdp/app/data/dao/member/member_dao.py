import uuid
from datetime import datetime

from bzscl.model.entity.member.asset_entity import AssetEntity
from bzscl.model.entity.member.device_entity import DeviceEntity
from bzscl.model.entity.member.member_entity import MemberEntity
from bzscl.model.entity.member.member_jwttoken_entity import MemberJWTTokenEntity
from bzscl.model.entity.member.portfolio_entity import PortfolioEntity
from bzscl.model.entity.interaction.news_analysis_has_been_read_entity import NewsAnalysisHasBeenReadEntity
from django.db import DatabaseError
from ncl.dal.dao.entity_base_dao import BaseDao
from ncl.utils.common.singleton import Singleton


class MemberDao(BaseDao, metaclass=Singleton):
    model_class = MemberEntity

    def __init__(self):
        super().__init__()

    def find_member_by_phone_number(self, phone_number: str) -> MemberEntity:
        member = MemberEntity.objects.filter(phone_number=phone_number).first()

        return member

    def register_member(self, phone_number: str, user_tag: str):
        member = MemberEntity(phone_number=phone_number, name='', email='', tag=user_tag)
        member.objects = True
        try:
            member.save()
            return member
        except DatabaseError:
            member.active = False

    def add_portfolio(self, member: MemberEntity, name: str):
        portfolio_model_entity = PortfolioEntity(member_id=member.id, name=name)
        portfolio_model_entity.save()
        return portfolio_model_entity.id

    def get_portfolios(self, member: MemberEntity):
        portfolios = PortfolioEntity.objects.filter(member_id=member)
        return portfolios

    def get_asset_count(self, portfolio: PortfolioEntity):
        count = AssetEntity.objects.filter(portfolio_id=portfolio).count()
        return count

    def delete_portfolio(self, portfolio_id: uuid):
        portfolio_model = PortfolioEntity.objects.filter(id=portfolio_id)

        portfolio_model.delete()

    def get_all_assets(self, member: MemberEntity):
        all_assets = AssetEntity.objects.filter(member_id=member).all()
        return all_assets

    def get_assets_by_portfolio(self, member: MemberEntity, portfolio_id: uuid):
        assets_by_portfolio_id_member_id = AssetEntity.objects.filter(member_id=member, portfolio_id=portfolio_id)
        return assets_by_portfolio_id_member_id

    def save_details_of_asset(self, member: MemberEntity, name: str, code: str,
                              parent_code: str, company_name: str, portfolio_id: uuid,
                              count: float, buy_price: float, date_time: datetime, daily_usd_price: float,
                              base_value: float, description: str):
        asset_model = AssetEntity(member_id=member.id, name=name, code=code, parent_code=parent_code,
                                  portfolio_id=portfolio_id, company_name=company_name, count=count,
                                  buy_price=buy_price, description=description,
                                  daily_usd_price=daily_usd_price, base_value=base_value)

        asset_model.save()
        return asset_model.id

    def get_asset_by_id(self, asset_id: uuid):
        asset_by_id = AssetEntity.objects.filter(id=asset_id).all()
        return asset_by_id

    # todo
    def update_asset(self, asset_id: uuid, name: str, code: str,
                     count: float, buy_price: float, date_time: datetime,
                     description: str, daily_usd_price: float):
        asset = AssetEntity.objects.filter(id=asset_id).first()
        asset.name = name
        asset.code = code
        asset.count = count
        asset.buy_price = buy_price
        asset.date_time = date_time
        asset.description = description
        asset.daily_usd_price = daily_usd_price
        asset.save()
        return asset

    def delete_asset(self, asset_id: uuid):
        asset = AssetEntity.objects.filter(id=asset_id)
        asset.delete()

    def delete_member_jwt_token(self, member: MemberEntity):

        member_jwt = MemberJWTTokenEntity.objects.filter(member_id=member)
        member_jwt.delete()

    def edit_profile(self, member: MemberEntity, name: str, last_name: str, image_url: str):
        profile = self.get_profile_by_member(member=member)
        profile.name = name
        profile.last_name = last_name
        profile.image_url = image_url
        profile.save()

    def get_profile_by_member(self, member: MemberEntity):
        member_profile = MemberEntity.objects.get(id=member.id, active=True)
        return member_profile

    def update_phone_number(self, member: MemberEntity, phone_number: str):
        member.objects = True
        try:
            member.phone_number = phone_number
            member.save()
        except Exception as e:
            member.objects = False
            print(e)

    def create_member_device_relation(self, member: MemberEntity, device: DeviceEntity):
        member.devices.add(device)
        member.save()

    def exist_tag(self, tag):
        tag_exist = MemberEntity.objects.filter(tag=tag)
        if tag_exist:
            return True
        else:
            return False
