from typing import List
from bzsdp.app.data.esdao.interaction.inflation_tracker.priceables_list_esdao import PriceablesListESDao
from ncl.utils.common.singleton import Singleton


class PriceablesListDal(metaclass=Singleton):
    def __init__(self) -> None:
        self.esdao = PriceablesListESDao()

    def get_priceables(self) -> List:
        return self.esdao.get_priceables_list()
