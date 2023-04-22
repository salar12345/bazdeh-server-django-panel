from django_grpc_framework import proto_serializers
from bzscl.proto.bazdeh.media.loan import loan_pb2
class SingleLoanResponseSerializer(proto_serializers.ProtoSerializer):
    class Meta:
        proto_class = loan_pb2.SingleLoan