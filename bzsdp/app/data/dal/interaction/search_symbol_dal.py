from bzsdp.app.data.dao.interaction.search.search_symbol_dao import SearchSymbolDao
from ncl.utils.common.singleton import Singleton
from django.db.models import QuerySet


class SearchSymbolDal(metaclass=Singleton):

    def __init__(self):
        super().__init__()
        self.dao = SearchSymbolDao()

    def search_symbol_by_code(self, query_string: str) -> QuerySet:
        return self.dao.search_symbol_by_code(query_string)
