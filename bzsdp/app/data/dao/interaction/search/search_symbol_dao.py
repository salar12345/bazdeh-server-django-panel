from bzscl.model.entity.structure.visual_item_entity import VisualItemEntity
from ncl.dal.dao.entity_base_dao import BaseDao
from ncl.utils.common.singleton import Singleton
from django.db.models import QuerySet, Q
from bzsdp.project.config import BZSDPConfig
from bzsdp.app.model.vo.interaction.search_vo import SearchVo


class SearchSymbolDao(BaseDao, metaclass=Singleton):

    @staticmethod
    def search_symbol_by_code(query_string: str) -> QuerySet:
        symbols = VisualItemEntity.objects.all().filter(
            Q(code__icontains=query_string) | Q(fa_name__icontains=query_string) | Q(
                en_name__icontains=query_string)).order_by(
            f'-{SearchVo.CREATION_TIME}').exclude(Q(parent_code="BZ_BOURSE") | Q(parent_code="BZ_FARABOURSE"))
        return symbols
