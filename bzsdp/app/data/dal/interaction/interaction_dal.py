from bzscl.model.entity.member.member_entity import MemberEntity
from ncl.utils.common.singleton import Singleton
from rest_framework.utils.serializer_helpers import ReturnDict
from bzsdp.app.data.dao.interaction.interaction_dao import InteractionDao
from bzsdp.app.data.rd_dao.interaction.interaction_rd_dao import InteractionRdDao


class InteractionDal(metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.rddao = InteractionRdDao()
        self.dao = InteractionDao()

    def get_active_vote(self):
        return self.dao.get_active_vote()

    def get_member_participate(self, gps_adid: str):
        return self.rddao.get_member_participate(gps_adid=gps_adid)

    def save_report(self, news_url: str) -> bool:
        return self.dao.save_report(news_url=news_url)

    def save_message(self, message: ReturnDict, member: MemberEntity) -> bool:
        return self.dao.save_message(message=message, member=member)

    # watchlist
    def get_all_watchlist_entity(self, member: MemberEntity):
        return self.dao.get_all_watchlist_entity(member=member)

    def delete_item_from_watchlist(self, member: MemberEntity, one_item_in_watchlist_code: str):
        self.dao.delete_item_from_watchlist(member=member, one_item_in_watchlist_code=one_item_in_watchlist_code)

    def save_code_to_watchlist(self, code: str, member: MemberEntity, parent_code: str):
        self.dao.save_code_to_watchlist(code=code, member=member, parent_code=parent_code)

    # vote
    def get_vote(self):
        question, question_id, multiple = self.dao.get_vote()
        return question, question_id, multiple

    def get_choices(self, id):
        choice_question_list, choice_id_list = self.dao.get_choices(id=id)
        return choice_question_list, choice_id_list

    def submit_vote(self, question_id, dismiss, is_member):
        self.dao.submit_vote(question_id=question_id, dismiss=dismiss, is_member=is_member)

    def submit_vote_and_choices(self, choices_id):
        self.dao.submit_vote_and_choices(choices_id=choices_id)

    def save_user_vote(self, gps_adid, question_id):
        self.rddao.save_user_vote(gps_adid=gps_adid, question_id=question_id)

    # like_dislike
    def do_like_dislike(self, news_analysis_id: str = None, gps_add_id: str = None, like_or_dislike: str = None):
        return self.dao.do_like_dislike(news_analysis_id=news_analysis_id, gps_add_id=gps_add_id,
                                        like_or_dislike=like_or_dislike)

    def save_news_bookmark(self, member: MemberEntity, news_id: str):
        return self.dao.save_news_bookmark(member=member, news_id=news_id)

    def get_news_bookmark_id_list(self, member: MemberEntity):
        return self.dao.get_news_bookmark_id_list(member=member)

    def delete_news_bookmark(self, member: MemberEntity, news_id: str) -> bool:
        return self.dao.delete_news_bookmark(member=member, news_id=news_id)

    def get_count_of_has_been_read_news_and_analysis(self, member: MemberEntity):
        return self.dao.get_count_of_has_been_read_news_and_analysis(member=member)

    def add_news_or_analysis_to_has_been_read_entity(self, member: MemberEntity, news_id, analysis_id):
        self.dao.add_news_or_analysis_to_has_been_read_entity(member=member, news_id=news_id, analysis_id=analysis_id)

    def get_news_analysis_like_dislike_count(self, news_id, analysis_id):
        return self.dao.get_news_analysis_like_dislike_count(news_id=news_id, analysis_id=analysis_id)

    def get_news_analysis_like_member_state(self, member: MemberEntity, news_id, analysis_id):
        return self.dao.get_news_analysis_like_member_state(member=member, news_id=news_id, analysis_id=analysis_id)

    def get_news_analysis_dislike_member_state(self, member: MemberEntity, news_id, analysis_id):
        return self.dao.get_news_analysis_dislike_member_state(member=member, news_id=news_id, analysis_id=analysis_id)

    def do_like(self, news_id, analysis_id, member: MemberEntity, state):
        self.dao.do_like(news_id=news_id, analysis_id=analysis_id, member=member, state=state)

    def do_dislike(self, news_id, analysis_id, member: MemberEntity, state):
        self.dao.do_dislike(news_id=news_id, analysis_id=analysis_id, member=member, state=state)
