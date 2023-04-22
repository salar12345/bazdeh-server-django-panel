from django.urls import path

from bzsdp.app.api.controller.inform.price_alarm.price_alarm_change_activate_controller import \
    PriceAlarmChangeActivateController
from bzsdp.app.api.controller.inform.price_alarm.price_alarm_change_repeated_controller import \
    PriceAlarmChangeRepeatedController
from bzsdp.app.api.controller.inform.price_alarm.price_alarm_delete_controller import PriceAlarmDeleteController
from bzsdp.app.api.controller.inform.price_alarm.price_alarm_editor_controller import PriceAlarmEditorController
from bzsdp.app.api.controller.inform.price_alarm.price_alarms_get_all_controller import PriceAlarmGetAllController
from bzsdp.app.api.controller.inform.price_alarm.price_alarm_get_by_name_controller import PriceAlarmGetByNameController
from bzsdp.app.api.controller.inform.price_alarm.price_alarm_set_controller import PriceAlarmSetController

urlpatterns = [
    path('set', PriceAlarmSetController.as_view()),
    path('change_activate', PriceAlarmChangeActivateController.as_view()),
    path('delete', PriceAlarmDeleteController.as_view()),
    path('edith', PriceAlarmEditorController.as_view()),
    path('all', PriceAlarmGetAllController.as_view()),
    path('change_repeated', PriceAlarmChangeRepeatedController.as_view()),
    path('by_name', PriceAlarmGetByNameController.as_view())


]
