import uuid

from bzscl.model.entity.interaction.bookmark_entity import BookmarkEntity
from bzscl.model.entity.interaction.member_message_entity import MemberMessageEntity
from bzscl.model.entity.interaction.news_analysis_has_been_read_entity import NewsAnalysisHasBeenReadEntity
from bzscl.model.entity.interaction.news_analysis_like_entity import NewsAnalysisLikeDisLikeEntity
from bzscl.model.entity.interaction.report_entity import ReportEntity
from bzscl.model.entity.interaction.vote_choices_entity import VoteChoicesEntity
from bzscl.model.entity.interaction.vote_questions_entity import VoteQuestionsEntity
from bzscl.model.entity.interaction.watch_item_entity import WatchItemEntity
from bzscl.model.entity.member.member_entity import MemberEntity
from django.db import DatabaseError
from ncl.dal.dao.entity_base_dao import BaseDao
from ncl.utils.common.singleton import Singleton
from rest_framework.utils.serializer_helpers import ReturnDict

from bzsdp.app.model.vo.interaction.interaction_vo import InteractionVO


class InteractionDao(BaseDao, metaclass=Singleton):
    def __init__(self):
        super().__init__()

    @staticmethod
    def get_active_vote() -> VoteQuestionsEntity:
        active_vote = VoteQuestionsEntity.objects.filter(is_active=True).select_related()
        return active_vote

    @staticmethod
    def save_report(news_url) -> bool:

        report = ReportEntity(news_url=news_url)

        report.objects = True
        try:
            report.save()
            return True
        except DatabaseError:
            report.active = False

            return False

    @staticmethod
    def save_message(message: ReturnDict, member: MemberEntity) -> bool:
        try:
            member_message = MemberMessageEntity.objects.create(title=message[InteractionVO.TITLE],
                                                                content=message[InteractionVO.CONTENT],
                                                                member=member)
            member_message.save()
            return True
        except DatabaseError:
            return False

    @staticmethod
    def save_news_bookmark(member: MemberEntity, news_id: str) -> bool:
        try:
            bookmark = BookmarkEntity.objects.create(news_id=news_id, member=member)
            bookmark.save()
            return True
        except DatabaseError:
            return False

    @staticmethod
    def get_news_bookmark_id_list(member: MemberEntity):
        return BookmarkEntity.objects.filter(member_id=member).values(InteractionVO.NEWS_ID)

    @staticmethod
    def delete_news_bookmark(member: MemberEntity, news_id: str) -> bool:
        try:
            BookmarkEntity.objects.filter(member=member, news_id=news_id).delete()
            return True
        except Exception as e:
            print(e)
            return False

    # watchlist & delete watchlist

    def get_all_watchlist_entity(self, member: MemberEntity):
        all_watchlist = WatchItemEntity.objects.filter(member=member).all()
        return all_watchlist

    def delete_item_from_watchlist(self, member: MemberEntity, one_item_in_watchlist_code: str):
        deleted_model = WatchItemEntity.objects.filter(member=member, item_code=one_item_in_watchlist_code)
        deleted_model.delete()

    def save_code_to_watchlist(self, code: str, member: MemberEntity, parent_code: str):
        watchlist = WatchItemEntity(item_code=code, member=member, parent_code=parent_code)
        watchlist.objects = True
        watch_entity = WatchItemEntity.objects.filter(member=member, item_code=code)
        if watch_entity:
            return True
        else:
            try:
                watchlist.objects = True
                watchlist.save()
            except DatabaseError:
                watchlist.active = False

    # vote

    def get_vote(self):

        question_entity = VoteQuestionsEntity.objects.filter(is_active=True)
        if question_entity:
            question_entity = question_entity[0]
            id = question_entity.id
            question = question_entity.question
            multiple = question_entity.multiple
            return question, id, multiple
        else:
            return "vote doesn't exists", False, False

    def get_choices(self, id):
        choices = VoteChoicesEntity.objects.filter(question_id=id).order_by('creation_time')
        len = VoteChoicesEntity.objects.filter(question_id=id).count()

        choice_question_list = []
        choice_id_list = []
        for i in range(len):
            choice_question_list.append(choices[i].choice)
            choice_id_list.append(choices[i].id)

        return choice_question_list, choice_id_list

    def submit_vote(self, question_id: str = "", dismiss: bool = False, is_member: bool = False):

        question_entity = VoteQuestionsEntity.objects.filter(id=question_id)

        if question_entity:
            question_entity = question_entity[0]
        if not dismiss:
            if question_entity.all_participant:
                question_entity.all_participant += 1
            else:
                question_entity.all_participant = 1

        if dismiss:
            if question_entity.no_participant:
                question_entity.no_participant += 1
            else:
                question_entity.no_participant = 1

        elif is_member:
            if question_entity.member_participant:
                question_entity.member_participant += 1
            else:
                question_entity.member_participant = 1

        else:
            if question_entity.device_participant:
                question_entity.device_participant += 1
            else:
                question_entity.device_participant = 1
        try:
            question_entity.save()
        except DatabaseError:
            question_entity.active = False

    def submit_vote_and_choices(self, choices_id: uuid = None):

        choice_entity = VoteChoicesEntity.objects.filter(id == choices_id)
        if choice_entity:
            choice_entity = choice_entity[0]

            if choice_entity.number_of_answers:
                choice_entity.number_of_answers += 1
            else:
                choice_entity.number_of_answers = 1

            try:
                choice_entity.save()
            except DatabaseError:
                choice_entity.active = False

    # like_dislike
    # def do_like_dislike(self, news_analysis_id: str = None, gps_add_id: str = None, like_or_dislike: str = None):
    #     news_analysis_like_model = NewsAnalysisLikeDisLikeEntity.objects.filter(
    #         news_analysis_id=news_analysis_id, gpsad_id_like=gps_add_id).first()
    #     news_analysis_dislike_model = NewsAnalysisLikeDisLikeEntity.objects.filter(
    #         news_analysis_id=news_analysis_id, gpsad_id_dislike=gps_add_id).first()
    #
    #     # user do like
    #     if like_or_dislike == NewsAnalysisLikeVO.LIKE:
    #         # user dont disliked
    #         if news_analysis_dislike_model is None:
    #             # user dont liked & disliked-->like
    #             if news_analysis_like_model is None:
    #                 news_analysis_like_row_model = NewsAnalysisLikeDisLikeEntity(news_analysis_id=news_analysis_id,
    #                                                                              gpsad_id_like=gps_add_id)
    #                 news_analysis_like_row_model.save()
    #                 return {"new_state": NewsAnalysisLikeVO.LIKE}
    #             # user dont disliked but liked -->unlike
    #             else:
    #                 NewsAnalysisLikeDisLikeEntity.objects.filter(news_analysis_id=news_analysis_id,
    #                                                              gpsad_id_like=gps_add_id).delete()
    #                 return {"new_state": NewsAnalysisLikeVO.NULL}
    #         else:
    #             NewsAnalysisLikeDisLikeEntity.objects.filter(news_analysis_id=news_analysis_id,
    #                                                          gpsad_id_dislike=gps_add_id).delete()
    #             news_analysis_like_row_model = NewsAnalysisLikeDisLikeEntity(news_analysis_id=news_analysis_id,
    #                                                                          gpsad_id_like=gps_add_id)
    #             news_analysis_like_row_model.save()
    #             return {"new_state": NewsAnalysisLikeVO.LIKE}
    #     else:
    #         if news_analysis_like_model is None:
    #             if news_analysis_dislike_model is None:
    #                 news_analysis_like_row_model = NewsAnalysisLikeDisLikeEntity(news_analysis_id=news_analysis_id,
    #                                                                              gpsad_id_dislike=gps_add_id)
    #                 news_analysis_like_row_model.save()
    #                 return {"new_state": NewsAnalysisLikeVO.DISLIKE}
    #             else:
    #                 NewsAnalysisLikeDisLikeEntity.objects.filter(news_analysis_id=news_analysis_id,
    #                                                              gpsad_id_dislike=gps_add_id).delete()
    #                 return {"new_state": NewsAnalysisLikeVO.NULL}
    #         else:
    #             NewsAnalysisLikeDisLikeEntity.objects.filter(news_analysis_id=news_analysis_id,
    #                                                          gpsad_id_like=gps_add_id).delete()
    #             news_analysis_like_row_model = NewsAnalysisLikeDisLikeEntity(news_analysis_id=news_analysis_id,
    #                                                                          gpsad_id_dislike=gps_add_id)
    #             news_analysis_like_row_model.save()
    #             return {"new_state": NewsAnalysisLikeVO.DISLIKE}

    def get_count_of_has_been_read_news_and_analysis(self, member: MemberEntity):
        news_has_been_read_count = NewsAnalysisHasBeenReadEntity.objects.filter(member_id_id=member.id,
                                                                                analysis_id=None).count()
        analysis_has_been_read_count = NewsAnalysisHasBeenReadEntity.objects.filter(member_id_id=member.id,
                                                                                    news_id=None).count()
        return news_has_been_read_count, analysis_has_been_read_count

    def add_news_or_analysis_to_has_been_read_entity(self, member: MemberEntity, news_id, analysis_id):
        news_exist = NewsAnalysisHasBeenReadEntity.objects.filter(member_id_id=member.id, news_id=news_id,
                                                                           analysis_id=analysis_id)
        if not news_exist:
            news_analysis_has_been_read_object = NewsAnalysisHasBeenReadEntity(member_id_id=member.id, news_id=news_id,
                                                                           analysis_id=analysis_id)
            news_analysis_has_been_read_object.save()

    def get_news_analysis_like_dislike_count(self, news_id, analysis_id):
        news_analysis_like_count = NewsAnalysisLikeDisLikeEntity.objects.filter(news_id=news_id,
                                                                                analysis_id=analysis_id,
                                                                                like_or_dislike_state=True).count()
        news_analysis_dislike_count = NewsAnalysisLikeDisLikeEntity.objects.filter(news_id=news_id,
                                                                                   analysis_id=analysis_id,
                                                                                   like_or_dislike_state=False).count()
        return news_analysis_like_count, news_analysis_dislike_count

    def get_news_analysis_like_member_state(self, member: MemberEntity, news_id, analysis_id):
        member_like_state = NewsAnalysisLikeDisLikeEntity.objects.filter(news_id=news_id, analysis_id=analysis_id,
                                                                      member=member, like_or_dislike_state=True)
        if member_like_state:
            return True
        else:
            return False

    def get_news_analysis_dislike_member_state(self, member: MemberEntity, news_id, analysis_id):
        member_dislike_state = NewsAnalysisLikeDisLikeEntity.objects.filter(news_id=news_id, analysis_id=analysis_id,
                                                                         member=member, like_or_dislike_state=False)
        if member_dislike_state:
            return True
        else:
            return False

    def do_like(self, news_id, analysis_id, member: MemberEntity, state):
        member_do_sth = NewsAnalysisLikeDisLikeEntity.objects.filter(news_id=news_id, analysis_id=analysis_id,
                                                                     member=member)
        if state:
            if member_do_sth:
                member_do_sth.delete()
            news_analysis_like_row_model = NewsAnalysisLikeDisLikeEntity(news_id=news_id, analysis_id=analysis_id,
                                                                         member=member, like_or_dislike_state=True)
            news_analysis_like_row_model.save()
        else:
            NewsAnalysisLikeDisLikeEntity.objects.filter(news_id=news_id, analysis_id=analysis_id,
                                                         member=member, like_or_dislike_state=True).delete()

    def do_dislike(self, news_id, analysis_id, member: MemberEntity, state):
        member_do_sth = NewsAnalysisLikeDisLikeEntity.objects.filter(news_id=news_id, analysis_id=analysis_id,
                                                                     member=member)
        if state:
            if member_do_sth:
                member_do_sth.delete()
            news_analysis_dislike_row_model = NewsAnalysisLikeDisLikeEntity(news_id=news_id, analysis_id=analysis_id,
                                                                            member=member, like_or_dislike_state=False)
            news_analysis_dislike_row_model.save()
        else:
            NewsAnalysisLikeDisLikeEntity.objects.filter(news_id=news_id, analysis_id=analysis_id,
                                                         member=member, like_or_dislike_state=False).delete()
