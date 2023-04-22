from ncl.dal.rddao.commons_base_rddao import CommonsBaseRDDao, RDKey
from ncl.utils.common.singleton import Singleton




class InteractionRdDao(CommonsBaseRDDao, metaclass=Singleton):
    MEMBER_ID_KEY = RDKey("vote_gps_adid:{gps_adid}", 60 * 60 * 24 * 7 * 2)

    def __init__(self) -> None:
        super().__init__()


    def save_user_vote(self, gps_adid: str, question_id: str):

        key = self.MEMBER_ID_KEY.key.format(gps_adid=gps_adid)

        self.client.set(key, question_id)


    def get_member_participate(self, gps_adid: str):


        key = self.MEMBER_ID_KEY.key.format(gps_adid=gps_adid)

        vote = self.client.get(key)
        return vote

