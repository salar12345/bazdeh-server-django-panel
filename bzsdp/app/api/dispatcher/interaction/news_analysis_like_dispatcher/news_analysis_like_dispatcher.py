from django.urls import path

from bzsdp.app.api.controller.interaction.news_analysis.news_analysis_do_dislike_controller import \
    NewsAnalysisDoDisLikeController
from bzsdp.app.api.controller.interaction.news_analysis.news_analysis_do_like_controller import \
    NewsAnalysisDoLikeController
from bzsdp.app.api.controller.interaction.news_analysis.news_analysis_like_data_controller import \
    NewsAnalysisLikeResponseController

urlpatterns = [
    path('like', NewsAnalysisDoLikeController.as_view()),
    path('dislike', NewsAnalysisDoDisLikeController.as_view()),
    path('data', NewsAnalysisLikeResponseController.as_view())
]
