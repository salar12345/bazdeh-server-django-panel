from rest_framework import serializers


class RelatedDepositRequestSerializer(serializers.Serializer):
    profit = serializers.IntegerField()  #
    minimum_inventory = serializers.IntegerField()  #

    class Meta:
        fields = ['profit', 'minimum_inventory']
