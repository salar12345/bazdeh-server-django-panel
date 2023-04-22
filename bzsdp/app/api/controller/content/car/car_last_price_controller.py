from ncl.utils.common.singleton import Singleton
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from bzsdp.app.adapter.grpc.car_price.car_price_adapter import CarAdapter
from bzsdp.app.adapter.grpc.car_price_old.car_price_old_adapter import CarPriceOldAdapter
from bzsdp.app.api.controller.base_api_view import BasePanelController
from bzsdp.app.api.serializer.content.car_price.car_last_price_request_serializer import CarLastPriceRequestSerializer
from bzsdp.app.api.serializer.content.car_price.car_last_price_response_serializer import CarLastPriceResponseSerializer
from bzsdp.app.api.serializer.content.car_price.car_price_response_serializer import CarPriceResponseSerializer
from bzsdp.app.logic.content.content_logic import ContentLogic
from bzsdp.app.model.vo.content.car_price_vo import CarPriceVO


class CarLastPriceController(BasePanelController, APIView, metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.old_adapter = CarPriceOldAdapter()
        self.logic = ContentLogic()
        self.adapter = CarAdapter()

    def get(self, request):
        try:
            cars_response = self.adapter.get_car_list()
            total_cars_dict_list = self.logic.serve_car_list_dictionary(cars_response)
            serialized_car = CarPriceResponseSerializer(data=total_cars_dict_list)
            try:
                return Response(serialized_car.initial_data, status=status.HTTP_200_OK)
            except:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        data = request.data

        serializer = CarLastPriceRequestSerializer(data=data)
        if serializer.is_valid():
            target_uris = serializer.data.get(CarPriceVO.TARGET_URIS)
            car_price_type = serializer.data.get(CarPriceVO.CAR_PRICE_TYPE)
            car_production_year = serializer.data.get(CarPriceVO.CAR_PRODUCTION_YEAR)
            cars_price = self.old_adapter.get_live_price(target_uris=target_uris,
                                                         price_type=car_price_type,
                                                         production_year=car_production_year)
            cars_price_model = self.logic.create_car_last_price_model(cars_price=cars_price.car_data_point)

            serialized_model = CarLastPriceResponseSerializer(cars_price_model, many=True)
            try:
                return Response(serialized_model.data, status=status.HTTP_200_OK)
            except:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
