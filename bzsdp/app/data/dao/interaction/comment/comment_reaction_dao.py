from typing import Optional

from django.db.models import Subquery, QuerySet
from ncl.dal.dao.entity_base_dao import BaseDao
from ncl.utils.common.singleton import Singleton

from bzscl.model.entity.interaction.comment_reaction_entity import CommentReactionEntity


class CommentReactionDao(BaseDao, metaclass=Singleton):
    model_class = CommentReactionEntity

    def all(self, *, qs: Optional[QuerySet] = None) -> QuerySet:
        if qs is None:
            return self.model_class.objects.all()
        return qs.all()

    def reverse(self, *, qs: Optional[QuerySet] = None) -> QuerySet:
        if qs is None:
            return self.model_class.objects.reverse()
        return qs.reverse()

    def filter(self, *, qs: Optional[QuerySet] = None, **filters) -> QuerySet:
        if qs is None:
            return self.model_class.objects.filter(**filters)
        return qs.filter(**filters)

    def last(self, *, qs: Optional[QuerySet] = None) -> CommentReactionEntity:
        if qs is None:
            return self.model_class.objects.last()
        return qs.last()

    def count(self, *, qs: Optional[QuerySet] = None) -> int:
        if qs is None:
            return self.model_class.objects.count()
        return qs.count()

    def order_by(self, *fields: str, qs: Optional[QuerySet] = None) -> QuerySet:
        if qs is None:
            return self.model_class.objects.order_by(*fields)
        return qs.order_by(*fields)

    def distinct(self, *fields: str, qs: Optional[QuerySet] = None) -> QuerySet:
        if qs is None:
            return self.model_class.objects.distinct(*fields)
        return qs.distinct(*fields)

    def values(self, *fields: str, qs: Optional[QuerySet] = None) -> QuerySet:
        if qs is None:
            return self.model_class.objects.values(*fields)
        return qs.values(*fields)

    @staticmethod
    def as_subquery(qs: QuerySet, /) -> Subquery:
        return Subquery(qs)
