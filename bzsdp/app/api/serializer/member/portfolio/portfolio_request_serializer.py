
from rest_framework import serializers


class PortfolioRequestSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=256)

    class Meta:
        fields = ['name']
