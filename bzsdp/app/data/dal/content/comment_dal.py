import uuid
from typing import Any, Optional

from bzscl.model.entity.member.member_entity import MemberEntity
from bzscl.model.entity.interaction.comment_entity import CommentEntity
from django.db.models import QuerySet
from ncl.utils.common.singleton import Singleton

from bzsdp.app.data.dao.interaction.comment.comment_dao import CommentDao
from bzsdp.app.data.rd_dao.interaction.comment_rd_dao import CommentRDDao


class CommentDal(metaclass=Singleton):
    def __init__(self):
        self.dao = CommentDao()
        self.rddao = CommentRDDao()

    def create(
            self,
            member: MemberEntity,
            content: str,
            news_or_analysis_id: str,
            reply_to: Optional[CommentEntity] = None,
            mentioned_member: Optional[MemberEntity] = None
    ) -> CommentEntity:
        return self.dao.create(member, content, news_or_analysis_id, reply_to, mentioned_member)

    def get(self, *, qs: Optional[QuerySet[CommentEntity]] = None, **filters) -> CommentEntity:
        return self.dao.get(qs=qs, **filters)

    def delete(self, obj: CommentEntity) -> None:
        self.dao.delete(obj)

    def filter(self, **filters) -> QuerySet:
        return self.dao.filter(**filters)

    def exists(self, **filters) -> bool:
        return self.filter(**filters).exists()

    def order_by(self, *fields: str, qs: Optional[QuerySet] = None) -> QuerySet:
        return self.dao.order_by(*fields, qs=qs)

    def exclude(self, *, qs: Optional[QuerySet] = None, **filters: str) -> QuerySet:
        return self.dao.exclude(qs=qs, **filters)

    def get_by_id(self, id_: str) -> CommentEntity:
        return self.dao.get_by_id(id_)

    def cache_comment(self, key: str, value: Any) -> None:
        self.rddao.set(key, value)

    def get_cached_comment(self, key: str) -> Any:
        return self.rddao.get(key)

    def create_reaction(self, member: MemberEntity, comment_id: uuid, upvote_or_downvote: bool):
        self.dao.create_reaction(member=member, comment_id=comment_id, upvote_or_downvote=upvote_or_downvote)

    def delete_reaction(self, member: MemberEntity, comment_id: uuid):
        self.dao.delete_reaction(member=member, comment_id=comment_id)

    def exists_reaction(self, member: MemberEntity, comment_id: uuid, upvote_or_downvote: bool):
        return self.dao.exists_reaction(member=member, comment_id=comment_id, upvote_or_downvote=upvote_or_downvote)

    def count_reaction(self, comment_id: uuid, upvote_or_downvote: bool):
        return self.dao.count_reaction(comment_id=comment_id, upvote_or_downvote=upvote_or_downvote)

    def get_news_or_analysis_comments(self, news_or_analysis_id: str):
        return self.dao.get_news_or_analysis_comments(news_or_analysis_id=news_or_analysis_id)

    def get_comment_by_id(self, comment_id: uuid):
        return self.dao.get_comment_by_id(comment_id=comment_id)

    def get_comment_replies(self, comment_id: uuid):
        return self.dao.get_comment_replies(comment_id=comment_id)
