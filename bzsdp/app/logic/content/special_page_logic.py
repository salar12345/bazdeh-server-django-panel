
from ncl.utils.common.singleton import Singleton
from ngl.utils.cache.instrument_cache import InstrumentCache


from bzsdp.app.adapter.grpc.publisher_serve.web_publisher_serve_adapter import WebPublisherServeAdaptor
from bzsdp.app.data.dal.content.content_dal import ContentDal
from bzsdp.project.config import BZSDPConfig
from bzsdp.utils.utils import Utils
from ntl.model.bourse.market_enums import MarketType
from bzsdp.app.adapter.grpc.post_serve.web_post_serve_adapter import WebPostServeAdapter
from bzsdp.app.model.vo.adapter.post_vo import PostVo
from bzsdp.app.model.vo.adapter.publisher_vo import PublisherVo


class SpecialPageLogic(metaclass=Singleton):
    target_market_list = {MarketType.BOURSE, MarketType.FARA_BOURSE}

    def __init__(self):
        self.web_post_adapter = WebPostServeAdapter()
        self.dal = ContentDal()
        self.web_publisher_adapter = WebPublisherServeAdaptor()
        self.instrument_cache = InstrumentCache(
            NGL_INSTRUMENT_CACHE_GRPC_URL=BZSDPConfig.GRPC_SERVE_HOST_INS,
            target_market_list=self.target_market_list,
            NGL_CACHE_INFO_REFRESH_INTERVAL_SECOND=BZSDPConfig.NGL_CACHE_INFO_REFRESH_INTERVAL_SECOND,
            HAS_MOST_TRADE_VALUE=True, HAS_MOST_TRADE_VOLUME=True,
            HAS_MOST_PRICE_PERCENT_CHANGES=True,
            HAS_MOST_MARKET_VALUE=True,
            HAS_MOST_INDEX_EFFECT=True,
            HAS_MOST_TRADED_PRICE=True
        )

    def get_news_post(self, date_time, page: int, source_type=0, priceables_in=None, topic_in=None):
        if page == 0 and date_time is None:
            date_time = Utils.get_datetime_now()
            date_time = Utils.get_string_datetime_from_datetime(date_time)
        if source_type == 0:
            post_list = self.web_post_adapter.simple_search(priceables_in=priceables_in, topic_in=topic_in,
                                                            datetime_proto=date_time, page=page)
            final_post_list = list()
            for post in post_list:
                publisher_info = self.web_publisher_adapter.get_publishers_by_uri(post.get(PostVo.PUBLISHER_URI))
                share_url = self._create_share_url(post.get(PostVo.URI))
                final_post_list = self._create_final_post_list(final_post_list, post, publisher_info, share_url)

        return final_post_list

    @staticmethod
    def _create_share_url(uri):
        uri = str(uri)
        share_url = "https://bazdeh.com/news/" + uri + "/بازده"
        return share_url

    def _create_final_post_list(self, final_post_list, post, publisher_info, share_url):
        post['share_url'] = share_url
        if publisher_info:
            post['publisher'] = dict()
            post['publisher'][PublisherVo.PUBLISHER_NAME] = publisher_info.get(PublisherVo.PUBLISHER_NAME)
            post['publisher'][PublisherVo.LOGO_URL] = publisher_info.get(PublisherVo.LOGO_URL)
            post['publisher'][PublisherVo.URI] = publisher_info.get(PublisherVo.URI)
        final_post_list.append(post)
        return final_post_list

    def get_all_special_page_subjects(self):
        return self.dal.get_all_special_page_subjects()
