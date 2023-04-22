from ncl.api.health_reporter_server import HealthReporter
from ncl.utils.common.singleton import Singleton

from bzsdp.app.data.dao.system.health_check_dao import HealthCheckDao
from bzsdp.app.data.esdao.system.health_check_esdao import HealthCheckESDao
from bzsdp.app.data.rd_dao.system.health_check_rd_dao import HealthCheckRDDao
from bzsdp.app.adapter.grpc.ghasedak.ghasedak_adapter import GhasedakAdapter
from bzsdp.app.adapter.grpc.car_price.car_price_adapter import CarAdapter
from bzsdp.app.adapter.grpc.post_serve.web_post_serve_adapter import WebPostServeAdapter
from bzsdp.app.adapter.grpc.publisher_serve.web_publisher_serve_adapter import WebPublisherServeAdaptor
from bzsdp.app.adapter.grpc.member_log.member_log_adaptor import MemberLogAdaptor
from bzsdp.app.model.vo.system.health_check_vo import HealthCheckVo
from bzsdp.shared.metrics.system.health_check import health_check_metrics


class HealthCheckLogic(metaclass=Singleton):
    def __init__(self):
        self.agent = HealthReporter(
            [
                HealthCheckDao(),
                HealthCheckESDao(),
                HealthCheckRDDao(),
                GhasedakAdapter(),
                CarAdapter(),
                WebPostServeAdapter(),
                WebPublisherServeAdaptor(),
                MemberLogAdaptor()
            ]
        )

    def get_server(self):
        return self.agent

    def set_metrics(self):
        report = self.agent.report_health()

        if report[HealthCheckVo.POSTGRESQL][HealthCheckVo.IS_HEALTHY]:
            health_check_metrics.POSTGRESQL_HEALTH.inc()
        else:
            health_check_metrics.POSTGRESQL_HEALTH.dec()

        health_check_metrics.POSTGRESQL_RESPONSE_TIME.observe(
            report[HealthCheckVo.POSTGRESQL][HealthCheckVo.RESPONSE_TIME_MS] / 1000
        )

        if report[HealthCheckVo.ELASTICSEARCH][HealthCheckVo.IS_HEALTHY]:
            health_check_metrics.ELASTICSEARCH_HEALTH.inc()
        else:
            health_check_metrics.ELASTICSEARCH_HEALTH.dec()

        health_check_metrics.ELASTICSEARCH_RESPONSE_TIME.observe(
            report[HealthCheckVo.ELASTICSEARCH][HealthCheckVo.RESPONSE_TIME_MS] / 1000
        )

        if report[HealthCheckVo.REDIS][HealthCheckVo.IS_HEALTHY]:
            health_check_metrics.REDIS_HEALTH.inc()
        else:
            health_check_metrics.REDIS_HEALTH.dec()

        health_check_metrics.REDIS_RESPONSE_TIME.observe(
            report[HealthCheckVo.REDIS][HealthCheckVo.RESPONSE_TIME_MS] / 1000
        )

        if report[HealthCheckVo.GHASEDAK][HealthCheckVo.IS_HEALTHY]:
            health_check_metrics.GHASEDAK_HEALTH.inc()
        else:
            health_check_metrics.GHASEDAK_HEALTH.dec()

        health_check_metrics.GHASEDAK_RESPONSE_TIME.observe(
            report[HealthCheckVo.GHASEDAK][HealthCheckVo.RESPONSE_TIME_MS] / 1000
        )

        if report[HealthCheckVo.GILLETE][HealthCheckVo.IS_HEALTHY]:
            health_check_metrics.GILLETE_HEALTH.inc()
        else:
            health_check_metrics.GILLETE_HEALTH.dec()

        health_check_metrics.GILLETE_RESPONSE_TIME.observe(
            report[HealthCheckVo.GILLETE][HealthCheckVo.RESPONSE_TIME_MS] / 1000
        )

        if report[HealthCheckVo.POST_SERVE][HealthCheckVo.IS_HEALTHY]:
            health_check_metrics.POST_SERVE_HEALTH.inc()
        else:
            health_check_metrics.POSTGRESQL_HEALTH.dec()

        health_check_metrics.POST_SERVE_RESPONSE_TIME.observe(
            report[HealthCheckVo.POST_SERVE][HealthCheckVo.RESPONSE_TIME_MS] / 1000
        )

        if report[HealthCheckVo.PUBLISHER_SERVE][HealthCheckVo.IS_HEALTHY]:
            health_check_metrics.PUBLISHER_SERVE_HEALTH.inc()
        else:
            health_check_metrics.PUBLISHER_SERVE_HEALTH.dec()

        health_check_metrics.PUBLISHER_SERVE_RESPONSE_TIME.observe(
            report[HealthCheckVo.PUBLISHER_SERVE][HealthCheckVo.RESPONSE_TIME_MS] / 1000
        )

        if report[HealthCheckVo.MEMBER_LOG][HealthCheckVo.IS_HEALTHY]:
            health_check_metrics.MEMBER_LOG_HEALTH.inc()
        else:
            health_check_metrics.MEMBER_LOG_HEALTH.dec()

        health_check_metrics.MEMBER_LOG_RESPONSE_TIME.observe(
            report[HealthCheckVo.MEMBER_LOG][HealthCheckVo.RESPONSE_TIME_MS] / 1000
        )
