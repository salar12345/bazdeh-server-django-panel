from ncl.utils.common.singleton import Singleton
import requests
from requests.models import Response
import json
from bzsdp.project.config import BZSDPConfig
from bzsdp.app.model.vo.adapter.porsline_vo import PorslineVo
from typing import Dict


class PorslineAdapter(metaclass=Singleton):

    @staticmethod
    def get_porsline_response(payload: str, headers: Dict, url: str = BZSDPConfig.PORSLINE_RESPONSE_ADDRESS) -> Response:
        response = requests.request(method=PorslineVo.POST, url=url, headers=headers, data=payload)

        return json.loads(response.text)
