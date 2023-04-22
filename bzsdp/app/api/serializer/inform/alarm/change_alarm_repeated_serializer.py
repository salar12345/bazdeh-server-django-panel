from rest_framework import serializers


class ChangeAlarmRepeatedSerializer(serializers.Serializer):
    alarm_id = serializers.UUIDField()

    class Meta:
        fields = ["alarm_id"]
