from rest_framework import serializers


class PortfolioResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()

    class Meta:
        fields = ['id']
