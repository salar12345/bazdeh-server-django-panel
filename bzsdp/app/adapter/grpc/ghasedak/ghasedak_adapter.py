from typing import Any, Dict, List, Optional, Union
from time import time

from bzscl.proto.bazdeh.ghasedak.ghasedak_pb2 import GhasedakResponse, GhasedakRequest
from bzscl.proto.bazdeh.ghasedak.ghasedak_pb2_grpc import GhasedakStub
from bzscl.model.enum.structure.app_component import ComponentGrandParent, ComponentParent, ComponentChild
from grpc import insecure_channel
from ncl.utils.common.singleton import Singleton
from ncl.api.health_reporter_agent import HealthReporterAgent

from bzsdp.project.config import BZSDPConfig
from bzsdp.app.model.vo.system.health_check_vo import HealthCheckVo


class GhasedakAdapter(HealthReporterAgent, metaclass=Singleton):
    weight = 100

    def send_ghasedak_notification(
        self,
        push_token_list: List,
        title: str,
        content: str,
        notification_type: Optional[Any] = None,
        grand_parent: Optional[ComponentGrandParent] = None,
        parent: Optional[ComponentParent] = None,
        child: Optional[ComponentChild] = None,
    ) -> Union[GhasedakResponse, None]:
        try:
            return self._send_ghasedak_request(
                push_token_list,
                title,
                content,
                notification_type,
                grand_parent,
                parent,
                child
            )
        except Exception:
            pass

    def report_health(self) -> Dict:
        try:
            start = time()
            self._send_ghasedak_request(['random_push_token'], 'Health check', 'Up and running?!')
            end = time()
            return {
                HealthCheckVo.IS_HEALTHY: True,
                HealthCheckVo.HEALTH: 1,
                HealthCheckVo.RESPONSE_TIME_MS: (end - start) * 1000
            }
        except Exception:
            return {
                HealthCheckVo.IS_HEALTHY: False,
                HealthCheckVo.HEALTH: 0,
                HealthCheckVo.RESPONSE_TIME_MS: -1
            }

    @staticmethod
    def _send_ghasedak_request(
            push_token_list: List,
            title: str,
            content: str,
            notification_type: Optional[Any] = None,
            grand_parent: Optional[ComponentGrandParent] = None,
            parent: Optional[ComponentParent] = None,
            child: Optional[ComponentChild] = None,
    ) -> Union[GhasedakResponse, None]:
        with insecure_channel(BZSDPConfig.GHASEDAK_SERVE_ADDRESS) as channel:
            stub = GhasedakStub(channel)
            request = GhasedakRequest(
                push_token_list=push_token_list,
                grand_parent=grand_parent,
                parent=parent,
                child=child,
                title=title,
                content=content,
                notification_type=notification_type
            )
            response = stub.GetPushToken(request)
            return response

