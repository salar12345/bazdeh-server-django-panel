from apscheduler.schedulers.blocking import BlockingScheduler
from ncl.utils.common.singleton import Singleton

from bzsdp.app.logic.inform.alarm_logic import AlarmLogic
from bzsdp.app.logic.system.health_check_logic import HealthCheckLogic
from bzsdp.project.config import BZSDPConfig


class SchedulerJobs(metaclass=Singleton):

    def __init__(self):
        super().__init__()
        self.scheduler = BlockingScheduler()
        self.health_check_logic = HealthCheckLogic()
        self.inform_logic = AlarmLogic()

    def do_jobs(self):
        self.scheduler.add_job(
            self.health_check_logic.set_metrics,
            'interval',
            minutes=BZSDPConfig.PROMETHEUS_SET_METRICS_INTERVAL_MINUTES
        )

        self.scheduler.add_job(
            self.inform_logic.send_inform_alarm,
            'interval',
            minutes=BZSDPConfig.INFORM_NOTIFICATION_TIME
        )

        self.scheduler.start()
