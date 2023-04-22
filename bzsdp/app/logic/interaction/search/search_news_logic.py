from ncl.utils.common.singleton import Singleton
from bzsdp.app.adapter.grpc.post_serve.web_post_serve_adapter import WebPostServeAdapter
from bzsdp.utils.utils import Utils
from typing import List
from datetime import datetime, timedelta
from bzsdp.project.config import BZSDPConfig


class SearchNewsLogic(metaclass=Singleton):

    def __init__(self):
        super().__init__()
        self.adapter = WebPostServeAdapter()

    def get_news_list(self, search_query: str, page_number: int, end_datetime: str) -> List | None:
        if page_number == 1 and end_datetime is None:
            end_datetime = Utils.get_datetime_now()
            end_datetime = Utils.get_string_datetime_from_datetime(end_datetime)

        start_datetime = datetime.strptime(end_datetime, BZSDPConfig.DATETIME_FORMAT) - timedelta(days=14)
        start_datetime = start_datetime.strftime(BZSDPConfig.DATETIME_FORMAT)

        news_list = self.adapter.search_by_query_string(query_string=search_query, page=page_number,
                                                        start_datetime=start_datetime, end_datetime=end_datetime)
        return news_list
