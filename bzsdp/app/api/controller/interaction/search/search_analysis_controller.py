from rest_framework.views import APIView, Response
from rest_framework.request import Request
from rest_framework import status
from ncl.utils.common.singleton import Singleton
from bzsdp.app.api.serializer.interaction.search.search_analysis_serializer import SearchAnalysisSerializer
from bzsdp.app.model.vo.interaction.search_vo import SearchVo
from bzsdp.app.logic.interaction.search.search_analysis_logic import SearchAnalysisLogic


class SearchAnalysisController(APIView, metaclass=Singleton):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.logic = SearchAnalysisLogic()

    def get(self, request: Request) -> Response:
        serializer = SearchAnalysisSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        search_query = serializer.data.get(SearchVo.QUERY_STRING)
        page_number = serializer.data.get(SearchVo.PAGE_NUMBER)
        end_datetime = serializer.data.get(SearchVo.END_DATETIME)

        analysis_list = self.logic.get_analysis_list(search_query, page_number, end_datetime)
        return Response(analysis_list, status=status.HTTP_200_OK)
