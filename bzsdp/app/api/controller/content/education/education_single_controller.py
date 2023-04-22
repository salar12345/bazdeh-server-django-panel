from rest_framework import status
from rest_framework.response import Response

from rest_framework.views import APIView

from bzsdp.app.adapter.grpc.education.education_adapter import EducationAdapter
from bzsdp.app.api.serializer.content.education.serializer_education_by_id import EducationByIdSerializer
from bzsdp.app.logic.content.education.education_logic import EducationLogic
from bzsdp.app.model.vo.content.education.education_vo import EducationVO


class EducationSingleController(APIView):

    def __init__(self):
        super().__init__()
        self.adapter = EducationAdapter()
        self.logic = EducationLogic()

    def get(self, request):

        query_params = request.query_params

        serializer = EducationByIdSerializer(data=query_params)

        if serializer.is_valid():
            education_single = self.adapter.get_single_education(education_id=serializer.data.get(EducationVO.EDUCATION_ID))
            serialized_response = self.logic.create_education_single_model(message=education_single)
            return Response(serialized_response, status=status.HTTP_200_OK)
        else:

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
