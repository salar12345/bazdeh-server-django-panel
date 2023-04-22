from rest_framework import serializers

from bzsdp.app.api.serializer.member.member_shallow_serializer import MemberShallowSerializer
from bzsdp.app.api.serializer.interaction.comment.comment_resource_id_serializer import CommentResourceIDSerializer


class CommentMentionNotificationDataSerializer(serializers.Serializer):
    comment = CommentResourceIDSerializer()
    member = MemberShallowSerializer()
    content = serializers.CharField()
