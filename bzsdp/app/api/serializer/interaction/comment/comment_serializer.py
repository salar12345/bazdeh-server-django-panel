from bzscl.model.entity.interaction.comment_entity import CommentEntity
from rest_framework import serializers


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentEntity
        fields = [
            'id',
            'member_id',
            'content',
            'reply_to',
            'commenter_name',
            'commenter_last_name',
            'commenter_tag',
            'commenter_image_url',
            'creation_time',
            'father_name',
            'father_last_name',
            'father_tag',
        ]

    member_id = serializers.CharField(source='member.id')
    reply_to = serializers.CharField(source='reply_to.id', required=False, allow_null=True)
    commenter_name = serializers.CharField(source='member.name')
    commenter_last_name = serializers.CharField(source='member.last_name')
    commenter_tag = serializers.CharField(source='member.tag')
    commenter_image_url = serializers.CharField(source='member.image_url')
    father_name = serializers.CharField(source='mentioned_member.name', required=False, allow_null=True)
    father_last_name = serializers.CharField(source='mentioned_member.last_name', required=False, allow_null=True)
    father_tag = serializers.CharField(source='mentioned_member.tag', required=False, allow_null=True)
