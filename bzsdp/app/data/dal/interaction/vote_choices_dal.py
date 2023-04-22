from typing import Optional

from bzscl.model.entity.interaction.vote_choices_entity import VoteChoicesEntity
from django.db.models import QuerySet
from ncl.utils.common.singleton import Singleton

from bzsdp.app.data.dao.interaction.vote.vote_choices_dao import VoteChoicesDao


class VoteChoicesDal(metaclass=Singleton):
    def __init__(self):
        self.dao = VoteChoicesDao()

    def get(self, *, qs: Optional[QuerySet[VoteChoicesEntity]] = None, **filters) -> VoteChoicesEntity:
        return self.dao.get(qs=qs, **filters)
