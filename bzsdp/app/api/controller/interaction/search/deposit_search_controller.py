from bzscl.model.enum.structure.search_category_type import SearchCategoryType
from rest_framework.views import APIView, Response

from bzsdp.app.adapter.grpc.deposit.deposit_adapter import DepositAdapter
from rest_framework.request import Request
from operator import itemgetter

from bzsdp.app.api.serializer.interaction.search.search_symbol_serializer import SearchSerializer
from bzsdp.app.model.vo.interaction.search_vo import SearchVo
from bzsdp.project.config import BZSDPConfig
from rest_framework import status


class DepositSearchController(APIView):

    def __init__(self):
        super().__init__()
        self.adapter = DepositAdapter()

    def get(self, request: Request):
        serializer = SearchSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        search_query = serializer.data.get(SearchVo.QUERY_STRING)
        page_number = serializer.data.get(SearchVo.PAGE_NUMBER) - 1

        deposit_list = self.adapter.search_on_deposit(name=search_query)
        result_list = []

        for deposit in deposit_list.search_result:
            added_dict = {}
            added_dict["name"] = deposit.name
            added_dict["code"] = deposit.deposit_id
            added_dict["company"] = deposit.company
            added_dict["parent"] = SearchCategoryType.BZ_DEPOSIT.value
            result_list.append(added_dict)

        sorted_lsit = sorted(result_list, key=itemgetter('name'), reverse=False)
        return Response(sorted_lsit[BZSDPConfig.SEARCH_PAGE_NUMBER * page_number:(
                                                                                         page_number + 1) * BZSDPConfig.SEARCH_PAGE_NUMBER],
                        status=status.HTTP_200_OK)
