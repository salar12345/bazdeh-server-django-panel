from rest_framework import serializers


class AssetSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=256)
    code = serializers.CharField(max_length=256)
    parent_code = serializers.CharField(max_length=256)
    portfolio_id = serializers.UUIDField()
    company_name = serializers.CharField(max_length=256, required=False)
    count = serializers.FloatField()
    buy_price = serializers.FloatField()
    date_time = serializers.DateTimeField()
    description = serializers.CharField(max_length=256, required=False)
    daily_usd_price = serializers.FloatField()
    base_value = serializers.FloatField()

    class Meta:
        fields = ['name', 'code', 'parent_code', 'portfolio_id', 'company_name', 'count',
                  'buy_price', 'daily_usd_price', 'base_value', 'date_time', 'description']
