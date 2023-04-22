from rest_framework import serializers


class InflationRateSerializer(serializers.Serializer):
    year = serializers.IntegerField()
    inflation_rate = serializers.FloatField()
