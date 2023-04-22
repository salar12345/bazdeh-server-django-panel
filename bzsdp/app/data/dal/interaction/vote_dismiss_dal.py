from json import loads, dumps
from typing import List, Union

from bzscl.model.entity.interaction.vote_questions_entity import VoteQuestionsEntity
from bzscl.model.entity.member.member_entity import MemberEntity
from ncl.utils.common.singleton import Singleton

from bzsdp.app.data.rd_dao.interaction.vote_dismiss_rd_dao import VoteDismissRDDao


class VoteDismissDal(metaclass=Singleton):
    def __init__(self):
        self.rddao = VoteDismissRDDao()

    def add(self, member: MemberEntity, question: VoteQuestionsEntity) -> None:
        if cache := self.rddao.get(question.id):
            data = loads(cache)
            data.append(str(member.id))
            data = dumps(data)
            self.rddao.set(question.id, data)
        else:
            data = dumps([str(member.id)])
            self.rddao.set(str(question.id), data)

    def get(self, question: VoteQuestionsEntity) -> Union[None, List]:
        if data := self.rddao.get(question.id):
            return loads(data)
