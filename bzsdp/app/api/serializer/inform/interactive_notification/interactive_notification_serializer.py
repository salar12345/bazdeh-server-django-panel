from typing import Dict

from rest_framework import serializers

from bzsdp.app.model.vo.inform.interactive_notification_vo import InteractiveNotificationVo
from bzsdp.app.model.enum.inform.interactive_notification_type import InteractiveNotificationType
from bzsdp.app.api.serializer.inform.interactive_notification.comment_reply_notification_data_serializer import \
    CommentReplyNotificationDataSerializer
from bzsdp.app.api.serializer.inform.interactive_notification.comment_upvote_notification_data_serializer import \
    CommentUpvoteNotificationDataSerializer
from bzsdp.app.api.serializer.inform.interactive_notification.comment_mention_notification_data_serializer import \
    CommentMentionNotificationDataSerializer


class InteractiveNotificationSerializer(serializers.Serializer):
    notification_type = serializers.SerializerMethodField()
    timestamp = serializers.FloatField()
    datetime = serializers.DateTimeField()
    data = serializers.SerializerMethodField()

    def get_notification_type(self, instance: Dict) -> str:
        return instance[InteractiveNotificationVo.TYPE].value

    def get_data(self, instance: Dict) -> Dict:
        if instance[InteractiveNotificationVo.TYPE] == InteractiveNotificationType.COMMENT_REPLY:
            return CommentReplyNotificationDataSerializer(instance[InteractiveNotificationVo.DATA]).data
        if instance[InteractiveNotificationVo.TYPE] == InteractiveNotificationType.COMMENT_MENTION:
            return CommentMentionNotificationDataSerializer(instance[InteractiveNotificationVo.DATA]).data
        if instance[InteractiveNotificationVo.TYPE] == InteractiveNotificationType.COMMENT_UP_VOTE:
            return CommentUpvoteNotificationDataSerializer(instance[InteractiveNotificationVo.DATA]).data
        if instance[InteractiveNotificationVo.TYPE] == InteractiveNotificationType.RIGHT_GAME_VOTE:
            return instance[InteractiveNotificationVo.DATA]
        if instance[InteractiveNotificationVo.TYPE] == InteractiveNotificationType.WRONG_GAME_VOTE:
            return instance[InteractiveNotificationVo.DATA]
