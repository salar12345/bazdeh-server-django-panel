from rest_framework import serializers

from bzscl.model.entity.interaction.comment_entity import CommentEntity


class NewsOrAnalysisCommentsRepliesSerializer(serializers.ModelSerializer):
    commenter_name = serializers.CharField()
    commenter_last_name = serializers.CharField()
    commenter_image_url = serializers.CharField()
    commenter_tag = serializers.CharField()
    upvote_count = serializers.IntegerField()
    state = serializers.BooleanField(allow_null=True)
    father_name = serializers.CharField()
    father_last_name = serializers.CharField()
    father_tag = serializers.CharField()

    class Meta:
        model = CommentEntity
        fields = ["id", "member_id", "content", "reply_to", "upvote_count", "state", "commenter_name",
                  "commenter_last_name", "commenter_tag", "father_name",
                  "father_last_name", "father_tag", "creation_time", "commenter_image_url"]


class NewsOrAnalysisCommentsResponseSerializer(serializers.ModelSerializer):
    commenter_name = serializers.CharField()
    commenter_last_name = serializers.CharField()
    commenter_image_url = serializers.CharField()
    commenter_tag = serializers.CharField()

    upvote_count = serializers.IntegerField()
    state = serializers.BooleanField(allow_null=True)

    replies = NewsOrAnalysisCommentsRepliesSerializer(many=True)

    class Meta:
        model = CommentEntity
        fields = ["id", "member_id", "content", "reply_to", "replies", "upvote_count", "state", "commenter_name",
                  "commenter_last_name", "commenter_tag", "creation_time", "commenter_image_url", "is_deleted"]
