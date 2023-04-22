from typing import Dict

from rest_framework import serializers

from bzscl.model.vo.interaction.comment_vo import CommentVo
from bzsdp.app.model.enum.inform.interactive_notification_resource_type import InteractiveNotificationResourceType


class CommentResourceIDSerializer(serializers.Serializer):
    comment_id = serializers.CharField()
    resource_id = serializers.CharField(source=CommentVo.NEWS_OR_ANALYSIS_ID)
    resource_type = serializers.SerializerMethodField()

    def get_resource_type(self, instance: Dict) -> str:
        if instance[CommentVo.NEWS_OR_ANALYSIS_ID][:8] == 'web_post':
            return InteractiveNotificationResourceType.NEWS.value
        return InteractiveNotificationResourceType.ANALYSIS.value
