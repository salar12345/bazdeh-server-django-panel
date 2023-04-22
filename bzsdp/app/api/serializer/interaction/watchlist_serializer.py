from bzscl.model.entity.interaction.watch_item_entity import WatchItemEntity
from rest_framework import serializers


class WatchlistSerializer(serializers.Serializer):
    item_code = serializers.CharField()
    parent_code = serializers.CharField(required=False)

    class Meta:
        fields = ['item_code', 'parent_code']


class WatchListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WatchItemEntity
        fields = '__all__'


