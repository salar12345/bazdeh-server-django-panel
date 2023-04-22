from django.urls import path

from bzsdp.app.api.controller.interaction.report.report_controller import ReportController

urlpatterns = [
    path('report', ReportController.as_view()),
]
