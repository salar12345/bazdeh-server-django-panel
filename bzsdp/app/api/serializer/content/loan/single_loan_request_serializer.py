from rest_framework import serializers


class SingleLoanRequesterializer(serializers.Serializer):

    loan_id = serializers.CharField()  #

    class Meta:
        fields = ['loan_id']
