from rest_framework import serializers


class SingleDepositRequesterializer(serializers.Serializer):
    deposit_id = serializers.CharField()  #

    class Meta:
        fields = ['deposit_id']
