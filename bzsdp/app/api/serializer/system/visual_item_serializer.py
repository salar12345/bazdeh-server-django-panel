from bzscl.model.entity.structure.visual_item_entity import VisualItemEntity
from rest_framework import serializers


class VisualItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisualItemEntity
        fields = '__all__'