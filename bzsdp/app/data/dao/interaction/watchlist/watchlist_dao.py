from bzscl.model.entity.interaction.watch_item_entity import WatchItemEntity
from bzscl.model.entity.member.member_entity import MemberEntity
from django.db import DatabaseError
from ncl.dal.dao.entity_base_dao import BaseDao
from ncl.utils.common.singleton import Singleton


class InteractionDao(BaseDao, metaclass=Singleton):
    def __init__(self):
        super().__init__()

    # watchlist & delete watchlist

    def get_all_watchlist_entity(self, member: MemberEntity):
        all_watchlist = WatchItemEntity.objects.filter(member=member).all()
        return all_watchlist

    def delete_item_from_watchlist(self, member: MemberEntity, one_item_in_watchlist_code: str):
        deleted_model = WatchItemEntity.objects.filter(member=member, item_code=one_item_in_watchlist_code)
        deleted_model.delete()

    def save_code_to_watchlist(self, code: str, member: MemberEntity, parent_code: str):
        watchlist = WatchItemEntity(item_code=code, member=member, parent_code=parent_code)
        watchlist.objects = True
        watch_entity = WatchItemEntity.objects.filter(member=member, item_code=code)
        if watch_entity:
            return True
        else:
            try:
                watchlist.objects = True
                watchlist.save()
            except DatabaseError:
                watchlist.active = False
