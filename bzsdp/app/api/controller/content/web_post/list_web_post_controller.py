from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_406_NOT_ACCEPTABLE
from rest_framework.request import Request
from rest_framework.response import Response

from bzsdp.app.logic.content.web_post_logic import WebPostLogic
from bzsdp.app.api.serializer.content.web_post.web_post_query_serializer import WebPostQuerySerializer


class ListWebPostController(APIView):
    def __init__(self, *args, **kwargs):
        self.web_post_logic = WebPostLogic()
        super().__init__(*args, **kwargs)

    def post(self, request: Request) -> Response:
        try:
            serializer = WebPostQuerySerializer(data=request.data)
            if serializer.is_valid():
                return Response(
                    self.web_post_logic.query_posts(**serializer.data),
                    HTTP_200_OK
                )
            else:
                return Response(serializer.errors, HTTP_406_NOT_ACCEPTABLE)
        except Exception:
            return Response(None, HTTP_400_BAD_REQUEST)
