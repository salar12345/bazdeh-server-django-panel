from bzscl.model.entity.content.special_page_entity import SpecialPageEntity
from rest_framework import serializers


class SpecialSubjectsSerializer(serializers.ModelSerializer):

    class Meta:
        model = SpecialPageEntity
        fields = '__all__'