
from django_grpc_framework import proto_serializers
from bzscl.proto.bazdeh.media.deposit import deposit_pb2


class ListDepositSerializer(proto_serializers.ProtoSerializer):
    class Meta:
        proto_class = deposit_pb2.ListDeposit


class DepositListSerializer(proto_serializers.ProtoSerializer):
    deposit_list = ListDepositSerializer(many=True)

    class Meta:
        proto_class = deposit_pb2.DepositListResponse
