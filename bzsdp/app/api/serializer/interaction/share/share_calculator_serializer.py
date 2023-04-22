from rest_framework import serializers
from bzsdp.app.model.vo.interaction.share_vo import ShareVo


class ShareCalculatorsContentSerializer(serializers.Serializer):
    subtitle = serializers.CharField()
    description = serializers.CharField(allow_blank=True)

    class Meta:
        fields = ShareVo.__ALL__


class ShareCalculatorsSerializer(serializers.Serializer):
    type_ = serializers.CharField()
    title = serializers.CharField()
    content = ShareCalculatorsContentSerializer(many=True)

    class Meta:
        fields = ShareVo.__ALL__
