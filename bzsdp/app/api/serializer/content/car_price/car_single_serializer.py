from django_grpc_framework import proto_serializers
from bzscl.proto.bazdeh.media.car_price.car_price_pb2 import CarSingletResponse


class CarSingleSerializer(proto_serializers.ProtoSerializer):

    class Meta:
        proto_class = CarSingletResponse
