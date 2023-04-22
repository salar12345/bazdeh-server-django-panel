from json import loads, dumps
from collections import OrderedDict

from ncl.utils.common.singleton import Singleton

from bzsdp.app.data.rd_dao.content.web_post_view_rddao import WebPostViewRDDao


class WebPostViewDal(metaclass=Singleton):
    def __init__(self):
        self.web_post_view_rddao = WebPostViewRDDao()

    def set(self, value: OrderedDict) -> None:
        self.web_post_view_rddao.set(dumps(value))

    def get(self) -> OrderedDict:
        if data := self.web_post_view_rddao.get():
            return OrderedDict(loads(data))
        else:
            return OrderedDict()
