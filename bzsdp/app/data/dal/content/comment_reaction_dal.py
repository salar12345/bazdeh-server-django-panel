from typing import Optional

from django.db.models import Subquery, QuerySet
from ncl.utils.common.singleton import Singleton
from bzscl.model.entity.interaction.comment_reaction_entity import CommentReactionEntity

from bzsdp.app.data.dao.interaction.comment.comment_reaction_dao import CommentReactionDao


class CommentReactionDal(metaclass=Singleton):
    def __init__(self):
        self.dao = CommentReactionDao()

    def all(self, *, qs: Optional[QuerySet] = None) -> QuerySet:
        return self.dao.all(qs=qs)

    def reverse(self, *, qs: Optional[QuerySet] = None) -> QuerySet:
        return self.dao.reverse(qs=qs)

    def filter(self, *, qs: Optional[QuerySet] = None, **filters) -> QuerySet:
        return self.dao.filter(qs=qs, **filters)

    def last(self, *, qs: Optional[QuerySet] = None) -> CommentReactionEntity:
        return self.dao.last(qs=qs)

    def count(self, *, qs: Optional[QuerySet] = None) -> int:
        return self.dao.count(qs=qs)

    def order_by(self, *fields: str, qs: Optional[QuerySet] = None) -> QuerySet:
        return self.dao.order_by(*fields, qs=qs)

    def distinct(self, *fields: str, qs: Optional[QuerySet] = None) -> QuerySet:
        return self.dao.distinct(*fields, qs=qs)

    def values(self, *fields: str, qs: Optional[QuerySet] = None) -> QuerySet:
        return self.dao.values(*fields, qs=qs)

    def as_subquery(self, qs: QuerySet, /) -> Subquery:
        return self.dao.as_subquery(qs)
