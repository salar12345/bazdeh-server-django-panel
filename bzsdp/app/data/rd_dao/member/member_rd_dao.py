from ncl.dal.rddao.commons_base_rddao import CommonsBaseRDDao, RDKey
import json

from ncl.utils.common.singleton import Singleton


class MemberRdDao(CommonsBaseRDDao, metaclass=Singleton):

    def __init__(self):
        super().__init__()

    OTP_KEY = RDKey("OTP_CODE:{noence}", 9000)
    MEMBER_ID_KEY = RDKey("member_id:{member_id}", 60 * 60 * 24 * 7 * 2)

    def save_sms_code(self, code: int, noence: str, phone_number: str):

        key = self.OTP_KEY.key.format(noence=noence)
        value = [code, phone_number]

        self.client.set(key, json.dumps(value), ex=self.OTP_KEY.ttl)
        return code



    def get_sms_code(self, noence: str):

        key = self.OTP_KEY.key.format(noence=noence)

        value = self.client.get(key)
        if value is None:
            return (None, None)

        (code, phone) = json.loads(value)

        return (code, phone)



    def get_user_searches(self, member_id):

        key = self.MEMBER_ID_KEY.key.format(member_id=member_id)

        searches = self.client.get(key)
        searches = json.loads(searches)
        return searches



    def save_user_search(self, member_id: str, search_word: str):

        key = self.MEMBER_ID_KEY.key.format(member_id=member_id)
        value = []

        searches_result = self.client.get(key)

        if searches_result == None:
            searches_result = []

        if len(searches_result) > 0:
            searches_result = json.loads(searches_result)


        if len(searches_result) < 3:
            value.extend(searches_result)
            value.append(search_word)
        else:
            value.extend(searches_result)
            value.pop(0)
            value.append(search_word)

        self.client.set(key, json.dumps(value), ex=self.MEMBER_ID_KEY.ttl)

