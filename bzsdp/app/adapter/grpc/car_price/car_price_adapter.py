from time import time
from typing import Dict

import grpc
from bzscl.proto.bazdeh.media.car_price import car_price_pb2_grpc, car_price_pb2
from ncl.utils.common.lru_ttl_cache import lru_ttl_cache
from ncl.utils.common.singleton import Singleton
from ncl.api.health_reporter_agent import HealthReporterAgent

from bzsdp.project.config import BZSDPConfig
from bzsdp.app.model.vo.system.health_check_vo import HealthCheckVo


class CarAdapter(HealthReporterAgent, metaclass=Singleton):
    weight = 100

    def __init__(self):
        super().__init__()

    @lru_ttl_cache(ttl_seconds=2 * 60 * 60)
    def get_car_list(self):
        with grpc.insecure_channel(BZSDPConfig.LOAN_SERVE_ADDRESS) as channel:
            stub = car_price_pb2_grpc.CarPriceServeStub(channel=channel)
            request = car_price_pb2.CarListQuery()
            responses = stub.GetCarList(request)

        return responses

    @lru_ttl_cache(ttl_seconds=2 * 60 * 60, maxsize=1000)
    def get_car_by_id(self, car_id):
        with grpc.insecure_channel(BZSDPConfig.LOAN_SERVE_ADDRESS) as channel:
            stub = car_price_pb2_grpc.CarPriceServeStub(channel=channel)
            request = car_price_pb2.CarIdleQuery(car_id=car_id)
            responses = stub.GetById(request)

        return responses

    @lru_ttl_cache(ttl_seconds=2 * 60 * 60, maxsize=1000)
    def get_single_car(self, name, model, production_year):
        with grpc.insecure_channel(BZSDPConfig.LOAN_SERVE_ADDRESS) as channel:
            stub = car_price_pb2_grpc.CarPriceServeStub(channel=channel)
            request = car_price_pb2.CarSingleQuery(name=name, model=model, production_year=production_year)
            responses = stub.GetCarSingle(request)

        return responses  # todo change it to response (no 's') because it is single

    @lru_ttl_cache(ttl_seconds=2 * 60 * 60, maxsize=1000)
    def search_car_by_name(self, name: str):
        with grpc.insecure_channel(BZSDPConfig.LOAN_SERVE_ADDRESS) as channel:
            stub = car_price_pb2_grpc.CarPriceServeStub(channel=channel)
            request = car_price_pb2.CarSearchQuery(name=name)
            responses = stub.GetCarSearch(request)

        return responses

    def report_health(self) -> Dict:
        try:
            start = time()
            with grpc.insecure_channel(BZSDPConfig.LOAN_SERVE_ADDRESS) as channel:
                stub = car_price_pb2_grpc.CarPriceServeStub(channel=channel)
                request = car_price_pb2.CarListQuery()
                responses = stub.GetCarList(request)
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
