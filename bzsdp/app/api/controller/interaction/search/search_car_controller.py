from rest_framework.views import APIView, Response
from rest_framework.request import Request
from rest_framework import status
from ncl.utils.common.singleton import Singleton
from bzsdp.app.api.serializer.interaction.search.search_car_serializer import SearchCarSerializer
from bzsdp.app.model.vo.interaction.search_vo import SearchVo
from bzsdp.app.adapter.grpc.car_price.car_price_adapter import CarAdapter
from bzsdp.app.api.serializer.interaction.search.car_list_proto_serializer import CarListProtoSerializer
from bzsdp.app.model.vo.content.car_price_vo import CarPriceVO


class SearchCarController(APIView, metaclass=Singleton):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.adapter = CarAdapter()

    def get(self, request: Request) -> Response:
        serializer = SearchCarSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        search_query = serializer.data.get(SearchVo.QUERY_STRING)

        car_list_response = self.adapter.search_car_by_name(name=search_query)
        serialized_car_list = CarListProtoSerializer(message=car_list_response)
        return Response(serialized_car_list.initial_data.get(CarPriceVO.CAR), status=status.HTTP_200_OK)
