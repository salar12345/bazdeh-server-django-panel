from django.urls import path

from bzsdp.app.api.controller.interaction.tool.gold_bubble_controller import GoldBubbleController


urlpatterns = [
    path('gold_bubble/', GoldBubbleController.as_view())
]