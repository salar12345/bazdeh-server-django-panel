from django.urls import path

from bzsdp.app.api.controller.interaction.news_bookmark.news_bookmark_controller import NewsBookmarkController
from bzsdp.app.api.controller.interaction.news_bookmark.news_bookmark_delete_controller import \
    NewsBookmarkDeleteController
from bzsdp.app.api.controller.interaction.news_bookmark.news_list_bookmark_controller import \
    NewsListBookmarkController

urlpatterns = [
    path("news", NewsBookmarkController().as_view()),
    path("news/delete", NewsBookmarkDeleteController().as_view()),
    path("news/news_id", NewsListBookmarkController().as_view())

]