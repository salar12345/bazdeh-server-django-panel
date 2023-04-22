
from django_grpc_framework import proto_serializers
from bzscl.proto.bazdeh.media.loan import loan_pb2


class LoanImportantSerializer(proto_serializers.ProtoSerializer):
    class Meta:
        proto_class = loan_pb2.ListLoan

class LoanListSerializer(proto_serializers.ProtoSerializer):
    loan_list = LoanImportantSerializer(many=True)

    class Meta:
        proto_class = loan_pb2.GetLoansListResponse
