from bzscl.model.enum.content.car_price_type import CarPriceType
from rest_framework import serializers


class CarPriceResponseSerializer(serializers.Serializer):
    target_uri = serializers.CharField()  #
    car_type_fa_name = serializers.CharField()  #
    price = serializers.IntegerField()  #
    date = serializers.DateTimeField()  #
    production_year = serializers.IntegerField()  #
    price_type = serializers.CharField()  #
    attribute = serializers.CharField()  #
    model_db_value = serializers.CharField()  #
    model_fa_name = serializers.CharField()  #
    brand_db_value = serializers.CharField()  #
    brand_fa_name = serializers.CharField()  #
    company_fa_name = serializers.CharField()  #

    class Meta:
        fields = ['target_uris', 'car_type_fa_name', 'price', 'date', 'production_year', 'price_type', 'attribute',
                  'model_db_value', 'model_fa_name', 'brand_db_value', 'brand_fa_name', 'company_fa_name']
