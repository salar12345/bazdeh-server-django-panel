from typing import Dict

from ncl.utils.common.singleton import Singleton

from bzsdp.app.data.dal.content.web_post_view_dal import WebPostViewDal
from bzsdp.app.model.vo.adapter.post_vo import PostVo


class ImportantWebPostLogic(metaclass=Singleton):
    def __init__(self):
        self.web_post_dal = WebPostViewDal()

    def increase_view_count(self, web_post: Dict) -> None:
        counter = self.web_post_dal.get()
        if not web_post[PostVo.IS_IMPORTANT]:
            try:
                counter[web_post[PostVo.URI]] += 1
            except KeyError:
                counter[web_post[PostVo.URI]] = 1
            finally:
                self.web_post_dal.set(counter)
        else:
            pass
