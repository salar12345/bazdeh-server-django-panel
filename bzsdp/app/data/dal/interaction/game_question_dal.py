from typing import Optional


from bzscl.model.entity.interaction.game_question_entity import GameQuestionEntity
from django.db.models import QuerySet
from ncl.utils.common.singleton import Singleton

from bzsdp.app.data.dao.interaction.game.game_question_dao import GameQuestionDao

class GameQuestionDal(metaclass=Singleton):
    def __init__(self):
        self.dao = GameQuestionDao()

    def filter(self, *, qs: Optional[QuerySet] = None, **filters) -> QuerySet:
        return self.dao.filter(qs=qs, **filters)

    def exclude(self, *, qs: Optional[QuerySet] = None, **filters) -> QuerySet:
        return self.dao.exclude(qs=qs, **filters)

    def get(self, *, qs: Optional[QuerySet] = None, **filters) -> GameQuestionEntity:
        return self.dao.get(qs=qs, **filters)

    def distinct(self, *fields: str, qs: Optional[QuerySet] = None) -> QuerySet:
        return self.dao.distinct(*fields, qs=qs)

    def values(self, *fields: str, qs: Optional[QuerySet] = None) -> QuerySet:
        return self.dao.values(*fields, qs=qs)
