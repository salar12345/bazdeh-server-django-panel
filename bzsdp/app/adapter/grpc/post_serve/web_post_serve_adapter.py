import grpc
from typing import List, Dict
from bzscl.proto.bazdeh.media.web.post_pb2_grpc import WebPostServeStub
from bzscl.proto.bazdeh.media.web.post_pb2 import (SimpleSearchQuery, SearchResponse, GetByUriListQuery,
                                                   StringWithDatetimeSearchQuery)
from ncl.utils.common.singleton import Singleton
from bzsdp.app.model.enum.web_media_type import MediaType
from bzsdp.app.model.vo.adapter.post_vo import PostVo
from bzsdp.project.config import BZSDPConfig
from bzsdp.utils.utils import Utils
from time import time
from ncl.api.health_reporter_agent import HealthReporterAgent
from bzsdp.app.model.vo.system.health_check_vo import HealthCheckVo
from bzsdp.app.adapter.grpc.publisher_serve.web_publisher_serve_adapter import WebPublisherServeAdaptor


class WebPostServeAdapter(HealthReporterAgent, metaclass=Singleton):
    weight = 100

    def __init__(self):
        self.stub = self._create_web_post_stub()
        self.web_publisher_adapter = WebPublisherServeAdaptor()

    @staticmethod
    def _create_web_post_stub():
        channel = grpc.insecure_channel(BZSDPConfig.POST_SERVE_ADDRESS)
        return WebPostServeStub(channel)

    def get_post_by_uri_list(self, uri_list: List[str]) -> List[Dict]:
        try:
            request = GetByUriListQuery(uri_list=uri_list)
            response: SearchResponse = self.stub.GetByUriList(request)
            return self._get_total_count_and_post_list_from_proto_response(response)
        except grpc.RpcError as error:
            print(error)

    # TODO: BUG
    def simple_search(self, datetime_proto, page: int, topic_in=[], priceables_in=[], is_important=0) -> List[Dict]:
        try:
            request = SimpleSearchQuery()
            request.page = page
            search_criteria = request.search_criteria
            search_criteria.is_important_type = is_important
            datetime_range = search_criteria.datetime_range
            datetime_range.datetime = datetime_proto
            datetime_range.datetime_type = datetime_range.DatetimeType.PUBLISH_DATETIME
            sort_field = request.sort_field
            sort_field.sort_field_type = 1
            if topic_in:
                for topic in topic_in:
                    topic_proto = search_criteria.topics_in_list.add()
                    topic_proto.topics.code = topic
            if priceables_in:
                for priceable in priceables_in:
                    priceable_proto = search_criteria.priceable_in_list.add()
                    priceable_proto.priceables.code = priceable
            response: SearchResponse = self.stub.SearchSimple(request)
            return self._get_total_count_and_post_list_from_proto_response(response)
        except grpc.RpcError as error:
            print(error)

    def search_by_query_string(self, query_string: str, page: int, start_datetime: str, end_datetime: str) -> List[Dict]:
        try:
            request = StringWithDatetimeSearchQuery()
            request.query_string = query_string
            request.page = page
            request.end_datetime = end_datetime
            request.start_datetime = start_datetime

            response: SearchResponse = self.stub.SearchByQueryString(request)
            news_list = self._get_total_count_and_post_list_from_proto_response(response)
            return self._make_final_news_list_for_query_search(news_list)

        except grpc.RpcError as exc:
            pass
        except Exception as exc2:
            pass

    def _make_final_news_list_for_query_search(self, news_list: List) -> List:
        for news in news_list:
            publisher_info = self.web_publisher_adapter.get_publishers_by_uri(news[PostVo.PUBLISHER_URI])
            if publisher_info:
                publisher_dict: Dict = dict()
                publisher_dict[PostVo.NAME] = publisher_info.get(PostVo.NAME)
                publisher_dict[PostVo.MEDIA_URL] = publisher_info.get(PostVo.MEDIA_URL)
                news[PostVo.PUBLISHER] = publisher_dict
        return news_list

    @staticmethod
    def _get_total_count_and_post_list_from_proto_response(response) -> List[Dict]:
        post_list: List = []
        proto_post_list = response.post_list
        for post in proto_post_list:
            post_dict: Dict = dict()
            post_dict[PostVo.IS_IMPORTANT] = post.is_important
            if uri := post.uri:
                post_dict[PostVo.URI]: str = uri
            if url := post.url:
                post_dict[PostVo.URL]: str = url
            if content := post.content:
                post_dict[PostVo.CONTENT]: str = content
            if title := post.title:
                post_dict[PostVo.TITLE]: str = title
            if caption := post.caption:
                post_dict[PostVo.CAPTION]: str = caption
            if media_list := post.media_list:
                post_dict[PostVo.MEDIA_LIST]: List = []
                for media in media_list:
                    media_dict: Dict = dict()
                    media_type = media.media_type
                    media_dict[PostVo.MEDIA_TYPE]: int = MediaType.get_media_type_from_grpc_code(media_type)
                    media_url = media.url
                    media_dict[PostVo.URL]: str = media_url
                    post_dict[PostVo.MEDIA_LIST].append(media_dict)
            if not media_list:
                post_dict[PostVo.MEDIA_LIST] = []
            if publisher_uri := post.publisher_uri:
                post_dict[PostVo.PUBLISHER_URI]: str = publisher_uri
            if html_content := post.html_content:
                post_dict[PostVo.HTML_CONTENT]: str = html_content
            if publish_datetime := post.publish_datetime:
                publish_datetime: str = Utils.standardize_string_datetime(publish_datetime)
                post_dict[PostVo.PUBLISH_DATETIME]: str = publish_datetime
            if creation_datetime := post.creation_datetime:
                creation_datetime: str = Utils.standardize_string_datetime(creation_datetime)
                post_dict[PostVo.CREATION_DATETIME]: str = creation_datetime
            if last_update_datetime := post.last_update_datetime:
                last_update_datetime: str = Utils.standardize_string_datetime(last_update_datetime)
                post_dict[PostVo.LAST_UPDATE_DATETIME]: str = last_update_datetime
            if topic_list := post.topics_list:
                post_dict[PostVo.TOPICS]: List = []
                for topic in topic_list:
                    topic_dict = dict()
                    if topic_code := topic.code:
                        topic_dict[PostVo.CODE] = topic_code
                    if topic_name := topic.name:
                        topic_dict[PostVo.NAME] = topic_name
                    post_dict[PostVo.TOPICS].append(topic_dict)
            if priceables_list := post.priceables_list:
                post_dict[PostVo.PRICEABLES]: List = []
                for priceable in priceables_list:
                    priceable_dict = dict()
                    if priceable_code := priceable.code:
                        priceable_dict[PostVo.CODE] = priceable_code
                    if priceable_persian_name := priceable.persian_name:
                        priceable_dict[PostVo.PERSIAN_NAME] = priceable_persian_name
                    post_dict[PostVo.PRICEABLES].append(priceable_dict)
            post_list.append(post_dict)
        return post_list

    def report_health(self) -> Dict:
        try:
            start = time()
            res = self.simple_search(Utils.get_string_datetime_from_datetime(Utils.get_datetime_now()), 1)
            end = time()
            if len(res) >= 0:
                return {
                    HealthCheckVo.IS_HEALTHY: True,
                    HealthCheckVo.HEALTH: 1,
                    HealthCheckVo.RESPONSE_TIME_MS: (end - start) * 1000
                }
        except Exception:
            return {
                HealthCheckVo.IS_HEALTHY: False,
                HealthCheckVo.HEALTH: 0,
                HealthCheckVo.RESPONSE_TIME_MS: -1
            }
