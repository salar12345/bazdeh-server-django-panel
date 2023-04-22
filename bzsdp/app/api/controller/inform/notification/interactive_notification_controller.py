from datetime import datetime

from ncl.utils.common.singleton import Singleton
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from bzsdp.app.api.controller.base_api_view import BasePanelController
from bzsdp.app.api.serializer.inform.interactive_notification.interactive_notification_serializer import InteractiveNotificationSerializer
from bzsdp.app.logic.inform.interactive_notification_logic import InteractiveNotificationLogic


class InteractiveNotificationController(BasePanelController, APIView, metaclass=Singleton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.interactive_notification_logic = InteractiveNotificationLogic()

    def post(self, request: Request) -> Response:
        try:
            return Response(
                InteractiveNotificationSerializer(
                    self.interactive_notification_logic.get_member_latest_notifications(
                        self.get_current_member(request),
                        datetime.fromtimestamp(request.data['timestamp'])
                    ),
                    many=True
                ).data,
                HTTP_200_OK
            )
        except Exception as e:
            raise e
            return Response(None, HTTP_400_BAD_REQUEST)
