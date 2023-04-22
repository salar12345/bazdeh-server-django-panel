from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from bzsdp.app.adapter.grpc.bazdeh_analysis.bazdeh_analysis_adapter import BazdehAnalysisAdapter


class AnalysisController(APIView):
    def __init__(self, **kwargs):
        self.bazdeh_analysis_adapter = BazdehAnalysisAdapter()
        super().__init__(**kwargs)

    def post(self, request: Request) -> Response:
        try:
            return Response(
                self.bazdeh_analysis_adapter.get_analysis_list(
                    int(request.data['page_number']),
                    request.data.get('last_creation_datetime')
                ),
                HTTP_200_OK
            )
        except Exception:
            return Response(None, HTTP_400_BAD_REQUEST)
