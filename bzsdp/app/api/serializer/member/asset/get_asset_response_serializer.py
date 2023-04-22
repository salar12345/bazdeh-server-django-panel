from bzscl.model.entity.member.asset_entity import AssetEntity
from rest_framework import serializers


class GetAssetResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetEntity
        fields = "__all__"
