from django.urls import path

from bzsdp.app.api.controller.interaction.game.game_question_active_controller import \
    GameQuestionActiveController
from bzsdp.app.api.controller.interaction.game.game_question_attended_inactive_controller import \
    GameQuestionAttendedInActiveController
from bzsdp.app.api.controller.interaction.game.game_question_not_attended_active_controller import \
    GameQuestionNotAttendedActiveController
from bzsdp.app.api.controller.interaction.game.game_question_attendance_controller import \
    GameQuestionAttendanceController
from bzsdp.app.api.controller.interaction.game.game_question_active_priceables_controller import \
    GameQuestionActivePriceablesController
from bzsdp.app.api.controller.interaction.game.game_question_last_attendance_result_controller import \
    GameQuestionLastAttendanceResultController

urlpatterns = [
    path('active', GameQuestionActiveController.as_view()),
    path('attendance', GameQuestionAttendanceController.as_view()),
    path('attended_inactive', GameQuestionAttendedInActiveController.as_view()),
    path('active_priceables', GameQuestionActivePriceablesController.as_view()),
    path('not_attended_active', GameQuestionNotAttendedActiveController.as_view()),
    path('last_attendance_result', GameQuestionLastAttendanceResultController.as_view())
]
