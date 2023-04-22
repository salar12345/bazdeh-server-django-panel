from rest_framework import serializers


class PortfolioGetSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    count = serializers.CharField(max_length=256)
    name = serializers.CharField(max_length=256)

    class Meta:
        fields = ['id', 'count', 'name']
