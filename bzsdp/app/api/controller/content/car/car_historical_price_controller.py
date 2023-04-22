from ncl.utils.common.singleton import Singleton
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from bzsdp.app.adapter.grpc.car_price_old.car_price_old_adapter import CarPriceOldAdapter
from bzsdp.app.api.controller.base_api_view import BasePanelController
from bzsdp.app.api.serializer.content.car_price.car_historical_price_request_serializer import \
    CarHistoricalPriceRequestSerializer
from bzsdp.app.api.serializer.content.car_price.car_historical_price_response_serializer import \
    CarHistoricalPriceResponseSerializer
from bzsdp.app.logic.content.content_logic import ContentLogic
from bzsdp.app.model.vo.content.car_price_vo import CarPriceVO
from bzsdp.app.utils.grpc.grpc_utils import GrpcUtils


class CarHistoricalPriceController(BasePanelController, APIView, metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.logic = ContentLogic()
        self.adapter = CarPriceOldAdapter()
        self.grpc_utils = GrpcUtils()

    def post(self, request):
        data = request.data
        serializer = CarHistoricalPriceRequestSerializer(data=data)
        if serializer.is_valid():
            target_uri = serializer.data.get(CarPriceVO.TARGET_URIS)
            price_type = serializer.data.get(CarPriceVO.CAR_PRICE_TYPE)
            production_year = serializer.data.get(CarPriceVO.CAR_PRODUCTION_YEAR)
            start_date_time, end_date_time = self.logic.create_historical_price_start_dateime_and_end_datetime()
            car_chart = self.adapter.get_car_historical_price_from_afra(targer_uri=target_uri,
                                                                        start_date_time=start_date_time,
                                                                        end_date_time=end_date_time,
                                                                        price_type=price_type,
                                                                        production_year=production_year)
            chart_points = []
            for point in car_chart.car_historical_price_point:
                chart_points.append(point.price_point)
            point_list = self.logic.create_car_historical_price_model(chart_points=chart_points)
            serialized_model = CarHistoricalPriceResponseSerializer(point_list, many=True)
            try:
                return Response(serialized_model.data, status=status.HTTP_200_OK)
            except:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
