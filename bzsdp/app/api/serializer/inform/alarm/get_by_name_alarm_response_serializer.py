from bzscl.model.entity.inform.alarm_entity import AlarmEntity
from rest_framework import serializers



class GetByNameAlarmsResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlarmEntity
        exclude = ("member", "current_price")


