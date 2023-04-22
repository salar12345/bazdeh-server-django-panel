import grpc
from bzscl.proto.bazdeh.media.bazdeh_education import education_pb2_grpc, education_pb2
from ncl.utils.common.singleton import Singleton

from bzsdp.project.config import BZSDPConfig


class EducationAdapter(metaclass=Singleton):
    def __init__(self):
        super().__init__()

    def get_page_education_list(self, page_number, last_creation_datetime):
        with grpc.insecure_channel(BZSDPConfig.EDUCATION_SERVE_ADDRESS) as channel:
            stub = education_pb2_grpc.BazdehEducationStub(channel=channel)
            request = education_pb2.GetEducationListRequest(page_number=page_number,
                                                            last_creation_datetime=last_creation_datetime)

            responses = stub.GetEducationList(request)

        return responses

    def get_single_education(self, education_id=str):
        with grpc.insecure_channel(BZSDPConfig.EDUCATION_SERVE_ADDRESS) as channel:
            stub = education_pb2_grpc.BazdehEducationStub(channel=channel)
            request = education_pb2.GetSingleEducationRequest(education_id=education_id)
            response = stub.GetSingleEducation(request)

        return response
