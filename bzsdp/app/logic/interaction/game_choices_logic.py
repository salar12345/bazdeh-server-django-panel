from ncl.utils.common.singleton import Singleton

from bzsdp.app.data.dal.interaction.game_choices_dal import GameChoicesDal


class GameChoicesLogic(metaclass=Singleton):
    def __init__(self):
        self.game_choices_dal = GameChoicesDal()
