from rest_framework import serializers
from bzscl.model.enum.content.car_price_type import CarPriceType


class CarHistoricalPriceRequestSerializer(serializers.Serializer):
    target_uris = serializers.CharField(max_length=32)  #
    price_type = serializers.ChoiceField(choices=CarPriceType, default=CarPriceType.ALL)  #
    production_year = serializers.IntegerField(allow_null=True, default=0)  #

    class Meta:
        fields = ['target_uris', 'car_price_type', 'car_production_year']
