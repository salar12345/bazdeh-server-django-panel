from bzscl.model.enum.content.car_price_type import CarPriceType
from rest_framework import serializers


class CarLastPriceResponseSerializer(serializers.Serializer):
    target_uri = serializers.UUIDField()  #
    car_type_fa_name = serializers.CharField()  #
    price = serializers.IntegerField()
    date = serializers.CharField()
    production_year = serializers.DateTimeField()
    price_type = serializers.CharField()
    # attribute = serializers.
    # model_db_value =
    # model_fa_name =
    # brand_db_value =
    # brand_fa_name =
    # company_fa_name =

    class Meta:
        fields = ['target_uris', 'car_type_fa_name', 'price', 'date', 'production_year', 'price_type', 'attribute',
                  'model_db_value', 'model_fa_name', 'brand_db_value', 'brand_fa_name', 'company_fa_name']
