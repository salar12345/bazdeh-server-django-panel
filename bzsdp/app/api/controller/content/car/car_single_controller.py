from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from bzsdp.app.adapter.grpc.car_price.car_price_adapter import CarAdapter
from bzsdp.app.api.controller.base_api_view import BasePanelController
from bzsdp.app.api.serializer.content.car_price.car_single_serializer import CarSingleSerializer
from bzsdp.app.logic.content.content_logic import ContentLogic
from bzsdp.app.model.vo.content.car_price_vo import CarPriceVO


class CarSingleController(BasePanelController, APIView):

    def __init__(self):
        super().__init__()
        self.logic = ContentLogic()
        self.adapter = CarAdapter()

    def get(self, request, *args, **kwargs):
        try:
            id_ = kwargs.get(CarPriceVO.ID)
            car = self.adapter.get_car_by_id(id_)
            serialized_car = CarSingleSerializer(message=car)
            return Response(serialized_car.initial_data, status=status.HTTP_200_OK)
        except Exception as exc:
            return Response(status=status.HTTP_400_BAD_REQUEST)
