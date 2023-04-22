from typing import Optional


from django.db.models import QuerySet
from ncl.utils.common.singleton import Singleton

from bzsdp.app.data.dao.interaction.game.game_choices_dao import GameChoicesDao



class GameChoicesDal(metaclass=Singleton):
    def __init__(self):
        self.dao = GameChoicesDao()

    def filter(self, *, qs: Optional[QuerySet] = None, **filters) -> QuerySet:
        return self.dao.filter(qs=qs, **filters)

    def exists(self, qs: Optional[QuerySet] = None, /) -> bool:
        return self.dao.exists(qs)
