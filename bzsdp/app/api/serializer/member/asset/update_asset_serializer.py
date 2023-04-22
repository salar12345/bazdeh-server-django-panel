from rest_framework import serializers


class UpdateAssetSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=256)
    code = serializers.CharField(max_length=256)
    count = serializers.FloatField()
    buy_price = serializers.FloatField()
    daily_usd_price = serializers.FloatField()
    date_time = serializers.DateTimeField()
    description = serializers.CharField(max_length=256, required=False)

    class Meta:
        fields = ['id', 'name', 'code', 'count',
                  'buy_price', 'daily_usd_price', 'date_time', 'description']
