from rest_framework import serializers

from bzscl.model.entity.member.member_entity import MemberEntity


class MemberShallowSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberEntity
        fields = ['name', 'last_name', 'tag']
