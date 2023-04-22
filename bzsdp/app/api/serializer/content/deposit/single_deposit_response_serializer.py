
from django_grpc_framework import proto_serializers
from bzscl.proto.bazdeh.media.deposit import deposit_pb2


class SingleDepositResponseSerializer(proto_serializers.ProtoSerializer):
    class Meta:
        proto_class = deposit_pb2.SingleDeposit
