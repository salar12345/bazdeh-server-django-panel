from rest_framework import serializers


class DeleteAssetSerializer(serializers.Serializer):
    id = serializers.UUIDField()

    class Meta:
        fields = ['id']
