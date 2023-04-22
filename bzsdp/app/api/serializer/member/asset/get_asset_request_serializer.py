from rest_framework import serializers


class GetAssetSerializer(serializers.Serializer):
    portfolio_id = serializers.UUIDField()

    class Meta:
        fields = ['portfolio_id']
