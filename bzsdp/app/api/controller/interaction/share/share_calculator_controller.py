from rest_framework.views import APIView, Response
from rest_framework.request import Request
from rest_framework import status
from bzsdp.app.api.controller.base_api_view import BasePanelController
from bzsdp.app.logic.interaction.share.share_calculator_logic import ShareCalculatorsLogic
from bzsdp.app.api.serializer.interaction.share.share_calculator_serializer import ShareCalculatorsSerializer


class ShareCalculatorsController(BasePanelController, APIView):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.logic = ShareCalculatorsLogic()

    def post(self, request: Request) -> Response:
        serializer = ShareCalculatorsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        share_image_url = self.logic.get_share_image_url(serializer.data)
        return Response(share_image_url, status=status.HTTP_200_OK)
        # todo : delete the result image after a while
