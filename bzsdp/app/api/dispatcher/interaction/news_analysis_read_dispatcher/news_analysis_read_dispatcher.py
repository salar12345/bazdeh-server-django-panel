from django.urls import path

from bzsdp.app.api.controller.interaction.news_analysis.news_analysis_read_controller import NewsAnalysisReadController


urlpatterns = [
    path('', NewsAnalysisReadController.as_view())
]
