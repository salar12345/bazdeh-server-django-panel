from rest_framework import serializers


class GetByNameAlarmRequestSerializer(serializers.Serializer):
    code = serializers.CharField()

    class Meta:
        fields = ["code"]
