from django.urls import path

from bzsdp.app.api.controller.interaction.comment.comment_controller import CommentController
from bzsdp.app.api.controller.interaction.comment.comment_upvote_downvote_controller import \
    CommentUpvoteDownvoteController
from bzsdp.app.api.controller.interaction.comment.first_comment_controller import FirstCommentController
from bzsdp.app.api.controller.interaction.comment.news_or_analysis_comments_controller import \
    NewsOrAnalysisCommentsController
from bzsdp.app.api.controller.interaction.comment.comment_delete_controller import CommentDeleteController

urlpatterns = [
    path('add', CommentController.as_view()),
    path('first', FirstCommentController.as_view()),
    path('delete', CommentDeleteController.as_view()),
    path('upvote_downvote', CommentUpvoteDownvoteController.as_view()),
    path('by_news_or_analysis', NewsOrAnalysisCommentsController.as_view())
]
