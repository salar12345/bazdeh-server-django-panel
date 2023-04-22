from bzscl.model.vo.content.news_vo import NewsVO
from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST
from rest_framework.request import Request
from rest_framework.response import Response

from bzsdp.app.adapter.grpc.post_serve.web_post_serve_adapter import WebPostServeAdapter
from bzsdp.app.logic.content.important_web_post_logic import ImportantWebPostLogic


class SingleWebPostController(APIView):
    def __init__(self, *args, **kwargs):
        self.web_post_serve_adapter = WebPostServeAdapter()
        self.important_web_post_logic = ImportantWebPostLogic()
        super().__init__(*args, **kwargs)

    def post(self, request: Request) -> Response:
        try:
            result = self.web_post_serve_adapter.get_post_by_uri_list([request.data.get(NewsVO.id)])
            if len(result) != 1:
                return Response(None, HTTP_404_NOT_FOUND)
            post = result[0]
            self.important_web_post_logic.increase_view_count(post)
            return Response(post, HTTP_200_OK)
        except Exception:
            return Response(None, HTTP_400_BAD_REQUEST)
