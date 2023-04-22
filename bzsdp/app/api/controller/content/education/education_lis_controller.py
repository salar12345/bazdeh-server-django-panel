from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from bzsdp.app.adapter.grpc.education.education_adapter import EducationAdapter
from bzsdp.app.api.serializer.content.education.education_serializer import EducationSerializer
from bzsdp.app.logic.content.education.education_logic import EducationLogic
from bzsdp.app.model.vo.content.education.education_vo import EducationVO


class EducationListController(APIView):

    def __init__(self):
        super().__init__()
        self.adapter = EducationAdapter()
        self.logic = EducationLogic()
    def get(self, request):

        query_parems = request.query_params

        serializer = EducationSerializer(data=query_parems)
        if serializer.is_valid():
            date_time = serializer.data.get(EducationVO.DATE_TIME)
            page_number =serializer.data.get(EducationVO.PAGE_NUMBER)
            education_list = self.adapter.get_page_education_list(page_number=page_number, last_creation_datetime=date_time)

            serialized_response = self.logic.create_education_model(education_list=education_list.education_list)

            return Response(serialized_response, status=status.HTTP_200_OK)

        else:

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
