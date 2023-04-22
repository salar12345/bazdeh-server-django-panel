from rest_framework import serializers


class DeletePortfolioSerializer(serializers.Serializer):
    id = serializers.UUIDField()

    class Meta:
        fields = ['id']
