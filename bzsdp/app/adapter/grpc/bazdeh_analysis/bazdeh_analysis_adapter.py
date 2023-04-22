import grpc
from typing import List, Dict, Optional
from bzscl.proto.bazdeh.media.bazdeh_analysis.bazdeh_analysis_pb2_grpc import BazdehAnalysisStub
from bzscl.proto.bazdeh.media.bazdeh_analysis.bazdeh_analysis_pb2 import ServeRequest, ServeByIdRequest
from bzscl.proto.bazdeh.media.web.post_pb2 import SearchResponse, StringWithDatetimeSearchQuery
from ncl.utils.common.singleton import Singleton
from bzsdp.app.model.vo.adapter.bazdeh_analysis_vo import BazdehAnalysisVO
from bzsdp.project.config import BZSDPConfig
from bzsdp.utils.utils import Utils


class BazdehAnalysisAdapter(metaclass=Singleton):

    def __init__(self):
        self.stub = self._create_analysis_stub()

    @staticmethod
    def _create_analysis_stub():
        channel = grpc.insecure_channel(BZSDPConfig.ANALYSIS_SERVE_ADDRESS)
        return BazdehAnalysisStub(channel)

    def get_analysis_list(self, page_number: int, last_creation_datetime: Optional[str] = None) -> List[Dict]:
        if last_creation_datetime is None:
            last_creation_datetime = Utils.get_string_datetime_from_datetime(Utils.get_datetime_now()).replace('T', ' ')
        request = ServeRequest()
        request.last_creation_datetime = last_creation_datetime
        request.page_number = page_number
        response = self.stub.ServeBazdehAnalysis(request)
        return self._get_analysis_list_from_proto_response(response)

    def get_analysis_single(self, analysis_id: str) -> Dict:
        request = ServeByIdRequest()
        request.Analysis_id = analysis_id
        response = self.stub.ServeBazdehAnalysisById(request)
        return self._turn_analysis_to_dict(response)

    def search_by_query_string(
            self,
            query_string: str,
            page: int,
            start_datetime: str,
            end_datetime: str
    ) -> List[Dict]:
        try:
            request = StringWithDatetimeSearchQuery()
            request.query_string = query_string
            request.page = page
            request.end_datetime = end_datetime
            request.start_datetime = start_datetime

            response: SearchResponse = self.stub.SearchByQueryString(request)
            return self._get_analysis_list_from_proto_response(response)

        except grpc.RpcError as exc:
            pass
        except Exception as exc2:
            pass

    @staticmethod
    def _turn_analysis_to_dict(analysis) -> Dict:
        analysis_dict = dict()

        if id_ := analysis.id:
            analysis_dict[BazdehAnalysisVO.ID]: str = id_

        if title := analysis.title:
            analysis_dict[BazdehAnalysisVO.TITLE]: str = title

        if content := analysis.content:
            analysis_dict[BazdehAnalysisVO.CONTENT]: str = content

        if url := analysis.url:
            analysis_dict[BazdehAnalysisVO.URL]: str = url

        if share_url := analysis.share_url:
            analysis_dict[BazdehAnalysisVO.SHARE_URL]: str = share_url

        if publish_datetime := analysis.publish_datetime:
            publish_datetime: str = Utils.standardize_string_datetime(publish_datetime)
            analysis_dict[BazdehAnalysisVO.PUBLISH_DATETIME]: str = publish_datetime

        # if update_datetime := analysis.update_datetime:
        #     analysis_dict[BazdehAnalysisVO.UPDATE_DATETIME]: str = update_datetime

        if media_url := analysis.media_url:
            analysis_dict[BazdehAnalysisVO.MEDIA_URL]: str = media_url

        if media_type := analysis.media_type:
            analysis_dict[BazdehAnalysisVO.MEDIA_TYPE]: str = media_type

        if creation_datetime := analysis.creation_datetime:
            creation_datetime: str = Utils.standardize_string_datetime(creation_datetime)
            analysis_dict[BazdehAnalysisVO.CREATION_DATETIME]: str = creation_datetime

        if summary := analysis.summary:
            analysis_dict[BazdehAnalysisVO.SUMMARY]: str = summary

        if like_count := analysis.like_count:
            analysis_dict[BazdehAnalysisVO.LIKE_COUNT]: str = like_count

        # if caption := analysis.caption:
        #     analysis_dict[BazdehAnalysisVO.CAPTION]: str = caption

        if priceables := analysis.priceables:
            analysis_dict[BazdehAnalysisVO.PRICEABLES]: List = []
            for priceable in priceables:
                priceable_dict = dict()
                if priceable_code := priceable.code:
                    priceable_dict[BazdehAnalysisVO.CODE] = priceable_code
                if priceable_persian_name := priceable.persian_name:
                    priceable_dict[BazdehAnalysisVO.PERSIAN_NAME] = priceable_persian_name
                analysis_dict[BazdehAnalysisVO.PRICEABLES].append(priceable_dict)

        if categories := analysis.category:
            analysis_dict[BazdehAnalysisVO.CATEGORIES]: List = []
            for category in categories:
                analysis_dict[BazdehAnalysisVO.CATEGORIES].append(category)

        publisher = {
            'name': 'بازده',
            'media_url': 'https://baazde.ir/images/baazde-logo.svg'
        }
        analysis_dict[BazdehAnalysisVO.PUBLISHER]: dict = publisher

        return analysis_dict

    @staticmethod
    def _get_analysis_list_from_proto_response(response) -> List[Dict]:
        analysis_list: List = []
        proto_analysis_list = response.analysis
        for analysis in proto_analysis_list:
            analysis_dict: Dict = dict()

            if id_ := analysis.id:
                analysis_dict[BazdehAnalysisVO.ID]: str = id_

            if title := analysis.title:
                analysis_dict[BazdehAnalysisVO.TITLE]: str = title

            if content := analysis.content:
                analysis_dict[BazdehAnalysisVO.CONTENT]: str = content

            if url := analysis.url:
                analysis_dict[BazdehAnalysisVO.URL]: str = url

            if share_url := analysis.share_url:
                analysis_dict[BazdehAnalysisVO.SHARE_URL]: str = share_url

            if publish_datetime := analysis.publish_datetime:
                publish_datetime: str = Utils.standardize_string_datetime(publish_datetime)
                analysis_dict[BazdehAnalysisVO.PUBLISH_DATETIME]: str = publish_datetime

            # if update_datetime := analysis.update_datetime:
            #     analysis_dict[BazdehAnalysisVO.UPDATE_DATETIME]: str = update_datetime

            if media_url := analysis.media_url:
                analysis_dict[BazdehAnalysisVO.MEDIA_URL]: str = media_url

            if media_type := analysis.media_type:
                analysis_dict[BazdehAnalysisVO.MEDIA_TYPE]: str = media_type

            if creation_datetime := analysis.creation_datetime:
                creation_datetime: str = Utils.standardize_string_datetime(creation_datetime)
                analysis_dict[BazdehAnalysisVO.CREATION_DATETIME]: str = creation_datetime

            if summary := analysis.summary:
                analysis_dict[BazdehAnalysisVO.SUMMARY]: str = summary

            if like_count := analysis.like_count:
                analysis_dict[BazdehAnalysisVO.LIKE_COUNT]: str = like_count

            # if caption := analysis.caption:
            #     analysis_dict[BazdehAnalysisVO.CAPTION]: str = caption

            if priceables := analysis.priceables:
                analysis_dict[BazdehAnalysisVO.PRICEABLES]: List = []
                for priceable in priceables:
                    priceable_dict = dict()
                    if priceable_code := priceable.code:
                        priceable_dict[BazdehAnalysisVO.CODE] = priceable_code
                    if priceable_persian_name := priceable.persian_name:
                        priceable_dict[BazdehAnalysisVO.PERSIAN_NAME] = priceable_persian_name
                    analysis_dict[BazdehAnalysisVO.PRICEABLES].append(priceable_dict)

            if categories := analysis.category:
                analysis_dict[BazdehAnalysisVO.CATEGORIES]: List = []
                for category in categories:
                    analysis_dict[BazdehAnalysisVO.CATEGORIES].append(category)

            publisher = {
                'name': 'بازده',
                'media_url': 'https://baazde.ir/images/baazde-logo.svg'
            }
            analysis_dict[BazdehAnalysisVO.PUBLISHER]: dict = publisher

            analysis_list.append(analysis_dict)

        return analysis_list
