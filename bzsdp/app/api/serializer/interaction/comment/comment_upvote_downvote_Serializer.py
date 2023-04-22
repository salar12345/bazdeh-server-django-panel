from rest_framework import serializers


class CommentUpvoteDownvoteSerializer(serializers.Serializer):
    comment_id = serializers.UUIDField()
    upvote_or_downvote = serializers.BooleanField()

    class Meta:
        fields = ["comment_id", "upvote_or_downvote"]
