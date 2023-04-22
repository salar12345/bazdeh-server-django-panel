from django.urls import path

from bzsdp.app.api.controller.content.analysis.single_analysis_controller import SingleAnalysisController
from bzsdp.app.api.controller.content.analysis.analysis_controller import AnalysisController

urlpatterns = [
    path('', AnalysisController.as_view()),
    path('single/', SingleAnalysisController.as_view())
]
