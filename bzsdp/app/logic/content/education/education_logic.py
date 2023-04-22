from typing import List, Dict

from google.protobuf.json_format import MessageToJson
from ncl.utils.common.singleton import Singleton

from bzscl.proto.bazdeh.media.bazdeh_education.education_pb2 import EducationModel
from rest_framework.utils import json



class EducationLogic(metaclass=Singleton):

    def create_education_model(self, education_list: List) -> List:
        result = []
        for education in education_list:
            json_model = MessageToJson(message=education)
            result.append(json.loads(json_model))
        return result

    def create_education_single_model(self, message: EducationModel) -> Dict:
        return json.loads(MessageToJson(message=message))
