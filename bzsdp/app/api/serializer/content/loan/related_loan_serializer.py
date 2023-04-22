from django_grpc_framework import proto_serializers
from bzscl.proto.bazdeh.media.loan import loan_pb2


class LoanRelatedSerializer(proto_serializers.ProtoSerializer):
    class Meta:
        proto_class = loan_pb2.RelatedLoan


class RelatedLoanSerializer(proto_serializers.ProtoSerializer):
    related_loan = LoanRelatedSerializer(many=True)

    class Meta:
        proto_class = loan_pb2.GetRelatedListResponse
