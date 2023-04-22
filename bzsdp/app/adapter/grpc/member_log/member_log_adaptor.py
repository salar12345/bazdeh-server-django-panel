from typing import Dict
from time import time

from bzscl.proto.bazdeh.member_log.member_log_pb2 import Ping, Pong
from bzscl.proto.bazdeh.member_log.member_log_pb2_grpc import ServicesStub
from grpc import insecure_channel
from ncl.utils.common.singleton import Singleton
from ncl.api.health_reporter_agent import HealthReporterAgent

from bzsdp.app.model.vo.system.health_check_vo import HealthCheckVo
from bzsdp.project.config import BZSDPConfig


class MemberLogAdaptor(HealthReporterAgent, metaclass=Singleton):
    weight = 100

    @staticmethod
    def report_health() -> Dict:
        try:
            with insecure_channel(BZSDPConfig.MEMBER_LOG_ADDRESS) as channel:
                request = Ping(sent=True)
                stub = ServicesStub(channel)
                start = time()
                response = stub.ReportHealth(request)
                end = time()
                if response.received:
                    return {
                        HealthCheckVo.IS_HEALTHY: True,
                        HealthCheckVo.HEALTH: 1,
                        HealthCheckVo.RESPONSE_TIME_MS: (end - start) * 1000
                    }
        except Exception:
            pass
        return {
            HealthCheckVo.IS_HEALTHY: False,
            HealthCheckVo.HEALTH: 0,
            HealthCheckVo.RESPONSE_TIME_MS: -1
        }
