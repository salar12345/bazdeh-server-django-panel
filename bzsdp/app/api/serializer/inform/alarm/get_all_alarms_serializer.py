from bzscl.model.entity.inform.alarm_entity import AlarmEntity
from rest_framework import serializers


class GetAllAlarmsSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()
    code = serializers.CharField()
    parent_code = serializers.CharField()
    alarm_price = serializers.FloatField()
    current_price = serializers.FloatField()
    notif_price = serializers.FloatField(allow_null=True, required=False)
    notif_datetime = serializers.DateTimeField(allow_null=True, required=False)
    date_time = serializers.DateTimeField()
    is_repeated = serializers.BooleanField()
    is_notify = serializers.BooleanField()
    is_more_than = serializers.BooleanField(allow_null=True, required=False)
    last_update_time = serializers.DateTimeField()
    is_deleted = serializers.BooleanField()

    class Meta:
        fields = ['id', 'name',
                  'code',
                  'parent_code', 'alarm_price', 'current_price', 'notif_price', 'notif_datetime', 'date_time',
                  'is_repeated', 'is_notify', 'is_more_than']
