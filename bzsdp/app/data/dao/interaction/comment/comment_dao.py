import uuid
from typing import Optional

from django.db.models import QuerySet
from ncl.dal.dao.entity_base_dao import BaseDao
from ncl.utils.common.singleton import Singleton

from bzscl.model.entity.interaction.comment_entity import CommentEntity
from bzscl.model.entity.interaction.comment_reaction_entity import CommentReactionEntity
from bzscl.model.entity.member.member_entity import MemberEntity


class CommentDao(BaseDao, metaclass=Singleton):
    model_class = CommentEntity

    def create(
            self,
            member: MemberEntity,
            content: str,
            news_or_analysis_id: str,
            reply_to: Optional[CommentEntity] = None,
            mentioned_member: Optional[MemberEntity] = None
    ) -> CommentEntity:
        return self.model_class.objects.create(
            member=member,
            content=content,
            news_or_analysis_id=news_or_analysis_id,
            reply_to=reply_to,
            mentioned_member=mentioned_member
        )

    @staticmethod
    def delete(obj: CommentEntity) -> None:
        obj.delete()

    def get(self, *, qs: Optional[QuerySet[CommentEntity]] = None, **filters) -> CommentEntity:
        if qs is None:
            return self.model_class.objects.get(**filters)
        return qs.get(**filters)

    def filter(self, **filters) -> QuerySet:
        return self.model_class.objects.filter(**filters)

    def exists(self, **filters) -> bool:
        return self.filter(**filters).exists()

    def order_by(self, *fields: str, qs: Optional[QuerySet] = None) -> QuerySet:
        if qs is None:
            return self.model_class.objects.order_by(*fields)
        return qs.order_by(*fields)

    def exclude(self, *, qs: Optional[QuerySet] = None, **filters: str) -> QuerySet:
        if qs is None:
            return self.model_class.objects.exclude(**filters)
        return qs.exclude(**filters)

    def create_reaction(self, member: MemberEntity, comment_id: uuid, upvote_or_downvote: bool):
        upvote_downvote_model = CommentReactionEntity(member_id=member.id, comment_id=comment_id,
                                                      status=upvote_or_downvote)
        upvote_downvote_model.objects = True
        try:
            upvote_downvote_model.objects = True
            upvote_downvote_model.save()
        except:
            upvote_downvote_model.active = False


    def delete_reaction(self, member: MemberEntity, comment_id: uuid):
        CommentReactionEntity.objects.filter(member_id=member.id, comment_id=comment_id).delete()

    def exists_reaction(self, member: MemberEntity, comment_id: uuid, upvote_or_downvote: bool):
        model = CommentReactionEntity.objects.filter(
            member_id=member.id, comment_id=comment_id, status=upvote_or_downvote).first()
        if model:
            return True
        else:
            return False


    def count_reaction(self, comment_id: uuid, upvote_or_downvote: bool):
        count = CommentReactionEntity.objects.filter(comment_id=comment_id, status=upvote_or_downvote).count()
        return count

    def get_news_or_analysis_comments(self, news_or_analysis_id: str):
        comments = CommentEntity.objects_all.filter(news_or_analysis_id=news_or_analysis_id, reply_to=None).order_by(
            '-creation_time')
        for comment in comments:
            if not CommentEntity.objects.filter(news_or_analysis_id=news_or_analysis_id,
                                                reply_to=comment.id) and CommentEntity.objects_all.filter(
                    news_or_analysis_id=news_or_analysis_id, id=comment.id, is_deleted=True):
                comments = comments.exclude(id=comment.id)

        return comments

    def get_comment_by_id(self, comment_id: uuid):
        comment = CommentEntity.objects.get(id=comment_id)
        return comment

    def get_comment_replies(self, comment_id: uuid):
        replies = CommentEntity.objects.filter(reply_to=comment_id).order_by('creation_time')
        return replies
