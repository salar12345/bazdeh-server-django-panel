from rest_framework import serializers


class ServePortfolioSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    current_value = serializers.FloatField()
    base_value = serializers.FloatField()


    class Meta:
        fields = ['id', 'current_value', 'base_value']