from ncl.utils.common.singleton import Singleton
from bzsdp.app.data.dal.interaction.search_symbol_dal import SearchSymbolDal
from django.db.models import QuerySet


class SearchSymbolLogic(metaclass=Singleton):

    def __init__(self):
        super().__init__()
        self.dal = SearchSymbolDal()

    def search_symbol_by_code(self, query_string: str) -> QuerySet:
        return self.dal.search_symbol_by_code(query_string)
