from django.urls import path

from bzsdp.app.api.controller.interaction.watch_list.delete_watchlist_controller import DeleteWatchlistController
from bzsdp.app.api.controller.interaction.watch_list.watchlist_controller import WatchlistController

urlpatterns = [
    path('', WatchlistController.as_view()),
    path("/delete", DeleteWatchlistController.as_view())
]