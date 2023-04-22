from rest_framework import serializers


class AssetIDSerializer(serializers.Serializer):
    id = serializers.UUIDField()

    class Meta:
        fields = ['id']
