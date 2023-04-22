
from django_grpc_framework import proto_serializers
from bzscl.proto.bazdeh.media.car_price import car_price_pb2


class ListCarSerializer(proto_serializers.ProtoSerializer):
    class Meta:
        proto_class = car_price_pb2.Car
class CarListProtoSerializer(proto_serializers.ProtoSerializer):
    car = ListCarSerializer(many=True)

    class Meta:
        proto_class = car_price_pb2.CarListResponse

