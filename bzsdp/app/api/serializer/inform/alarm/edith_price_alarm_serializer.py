from rest_framework import serializers


class EdithPriceAlarmSerializer(serializers.Serializer):
    alarm_id = serializers.UUIDField()
    alarm_price = serializers.FloatField()
    now_price = serializers.FloatField()
    name = serializers.CharField()
    code = serializers.CharField()
    parent_code = serializers.CharField()
    is_repeated = serializers.BooleanField()
    is_notify = serializers.BooleanField()

    class Meta:
        fields = ["alarm_price", 'now_price', 'notif_price', 'name', 'code', 'parent_code', 'is_repeated', 'is_notify']
