from typing import Any

from django.core.management.base import BaseCommand
from prometheus_client import start_http_server

from bzsdp.shared.scheduler.scheduler_jobs import SchedulerJobs
from bzsdp.project.config import BZSDPConfig


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> None:
        start_http_server(BZSDPConfig.PROMETHEUS_PORT)
        SchedulerJobs().do_jobs()
