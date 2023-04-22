from typing import Dict, List, Optional

from ncl.utils.common.singleton import Singleton

from bzsdp.utils.utils import Utils
from bzsdp.app.adapter.grpc.post_serve.web_post_serve_adapter import WebPostServeAdapter
from bzsdp.app.adapter.grpc.publisher_serve.web_publisher_serve_adapter import WebPublisherServeAdaptor
from bzsdp.app.model.vo.adapter.post_vo import PostVo
from bzsdp.app.model.vo.content.publisher_vo import PublisherVO


class WebPostLogic(metaclass=Singleton):
    def __init__(self):
        self.web_post_serve_adapter = WebPostServeAdapter()
        self.web_publisher_serve_adaptor = WebPublisherServeAdaptor()

    def query_posts(
            self,
            page_number: int,
            target_uris: List[str],
            category_types: List[str],
            first_creation_datetime: Optional[str] = None
    ) -> List[Dict]:
        query_dict = dict()
        topic_in, priceables_in = Utils.change_input_topic_and_pirceables(target_uris, category_types)
        query_dict['topic_in'] = topic_in
        query_dict['priceables_in'] = priceables_in
        query_dict['datetime_proto'] = first_creation_datetime.replace(
            'T',
            ' '
        ) if first_creation_datetime is not None else None
        query_dict['page'] = page_number

        for web_post in (web_posts := self.web_post_serve_adapter.simple_search(**query_dict)):
            self._add_publisher_info_to_web_post(web_post)

        return web_posts

    def _add_publisher_info_to_web_post(self, web_post: Dict) -> None:
        publisher_info = self.web_publisher_serve_adaptor.get_publishers_by_uri(web_post[PostVo.PUBLISHER_URI])
        publisher_info.pop(PublisherVO.CREATION_DATETIME, None)
        publisher_info.pop(PublisherVO.LAST_UPDATE_DATETIME, None)
        web_post[PostVo.PUBLISHER] = publisher_info
