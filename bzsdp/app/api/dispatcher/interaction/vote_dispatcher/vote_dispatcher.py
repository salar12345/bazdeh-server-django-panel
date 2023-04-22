from django.urls import path

from bzsdp.app.api.controller.interaction.vote.vote_controller import VoteController

urlpatterns = [
    path('', VoteController.as_view())
]
