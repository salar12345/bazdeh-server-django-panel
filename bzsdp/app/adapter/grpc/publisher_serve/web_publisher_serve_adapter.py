from time import time
from typing import Dict

import grpc
from bzscl.proto.bazdeh.media.web.publisher_pb2_grpc import WebPublisherServeStub
from bzscl.proto.bazdeh.media.web.publisher_pb2 import GetPublisherByUriQuery, GetPublisherByUriResponse
from ncl.api.health_reporter_agent import HealthReporterAgent
from ncl.utils.common.singleton import Singleton

from bzsdp.utils.utils import Utils
from bzsdp.app.model.vo.adapter.publisher_vo import PublisherVo
from bzsdp.project.config import BZSDPConfig
from bzsdp.app.model.vo.system.health_check_vo import HealthCheckVo


class WebPublisherServeAdaptor(HealthReporterAgent, metaclass=Singleton):
    weight = 100

    def __init__(self):
        self.stub = self._create_web_publisher_stub()

    @staticmethod
    def _create_web_publisher_stub():
        channel = grpc.insecure_channel(BZSDPConfig.PUBLISHER_SERVE_ADDRESS)
        return WebPublisherServeStub(channel)

    def get_publishers_by_uri(self, uri: str) -> Dict:
        try:
            request = GetPublisherByUriQuery()
            request.uri = uri
            response: GetPublisherByUriResponse = self.stub.GetPublisherByUri(request)
            return self._convert_publisher_proto_to_dictionary(response)
        except grpc.RpcError as error:
            print(error)
            # Utils.raise_grpc_exception_for_different_status_code(error)

    @staticmethod
    def _convert_publisher_proto_to_dictionary(publisher) -> Dict:
        publisher_dict: Dict = dict()
        if creation_datetime := publisher.creation_datetime:
            creation_datetime = Utils.standardize_string_datetime(creation_datetime)
            publisher_dict[PublisherVo.CREATION_DATETIME]: str = creation_datetime
        if last_update_datetime := publisher.last_update_datetime:
            last_update_datetime = Utils.standardize_string_datetime(last_update_datetime)
            publisher_dict[PublisherVo.LAST_UPDATE_DATETIME]: str = last_update_datetime
        if uri := publisher.uri:
            publisher_dict[PublisherVo.URI]: str = uri
        if publisher_name := publisher.publisher_name:
            publisher_dict[PublisherVo.PUBLISHER_NAME]: str = publisher_name
        if url := publisher.url:
            publisher_dict[PublisherVo.URL]: str = url
        if logo_url := publisher.logo_url:
            publisher_dict[PublisherVo.LOGO_URL]: str = logo_url
        return publisher_dict

    def report_health(self) -> Dict:
        try:
            start = time()
            self.get_publishers_by_uri('web_publisher:iranjib.ir')
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


if __name__ == '__main__':
    print(WebPublisherServeAdaptor().get_publishers_by_uri(uri="web_publisher:donya-e-eqtesad.com"))
