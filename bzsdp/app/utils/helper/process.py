from workers import task
from background_task import background
from django.contrib.auth.models import User

from bzsdp.app.logic.inform.alarm_logic import AlarmLogic


@task(schedule=60*5)
def run_alarm():
    AlarmLogic.send_alarm_price_notification()

@background(schedule=60*5)
def run_alarm():
    AlarmLogic.send_alarm_price_notification()