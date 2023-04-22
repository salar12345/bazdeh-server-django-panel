from rest_framework import serializers


class CarHistoricalPriceResponseSerializer(serializers.Serializer):
    price = serializers.IntegerField()  #
    date = serializers.DateTimeField()  #

    class Meta:
        fields = ['price', 'date']
