from rest_framework import serializers


class DeleteAlarmSerializer(serializers.Serializer):
    alarm_id = serializers.UUIDField()

    class Meta:
        fields = ["alarm_id"]
