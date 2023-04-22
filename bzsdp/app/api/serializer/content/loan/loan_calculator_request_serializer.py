from rest_framework import serializers


class LoanCalculatorRequestSerializer(serializers.Serializer):
    loan_amount = serializers.FloatField()  #
    profit = serializers.FloatField()  #
    num_of_installment = serializers.IntegerField()  #

    class Meta:
        fields = ['loan_amount', 'profit', 'num_of_installment']

