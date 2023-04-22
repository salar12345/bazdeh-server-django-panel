from rest_framework import serializers
from bzscl.model.enum.content.car_price_type import CarPriceType




class CarLastPriceRequestSerializer(serializers.Serializer):
    target_uri = serializers.ListField(child=serializers.CharField(), allow_null=True, required=False)
    car_price_type = serializers.CharField(default=CarPriceType.ALL, allow_null=True, required=False)  #
    car_production_year = serializers.IntegerField(default=0, allow_null=True, required=False)  #

    class Meta:
        fields = ['target_uri', 'car_price_type', 'car_production_year']
