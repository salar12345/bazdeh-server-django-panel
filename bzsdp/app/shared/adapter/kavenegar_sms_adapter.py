class SmsService:
    def send_verification_sms(self, phone_number: str, code: int) -> int:
        return True


from kavenegar import *
from bzsdp.project.config import BZSDPConfig


class KaveNegarService:

    @classmethod
    def send_sms(cls, phone_number: str, code: int):
        try:
            import json
        except ImportError:
            import simplejson as json
        try:
            api = KavenegarAPI(BZSDPConfig.Kave_Negar_API_Key)
            params = {
                'receptor': phone_number,
                'token': code,
                'template': BZSDPConfig.SMS_VERIFICATION_TEMPLATE,
                'verify': False,

            }
            response = api.verify_lookup(params)
            return response

        except APIException as e:
            print(e)
            return False

        except HTTPException as e:
            print(e)
            return False


class SmsServiceAdapter(SmsService):

    def __init__(self, kave_negar_service: KaveNegarService) -> None:
        super().__init__()
        self.kave_negar_adapter = kave_negar_service

    def send_verification_sms(self, phone_number: str, code: int):
        return self.kave_negar_adapter.send_sms(phone_number, code)
