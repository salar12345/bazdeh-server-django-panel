from bzscl.model.entity.interaction.game_question_entity import GameQuestionEntity
from rest_framework import serializers

from bzsdp.app.model.vo.interaction.game_vo import GameVo
from bzsdp.app.api.serializer.interaction.game.related_game_choices_serializer import RelatedGameChoicesSerializer


class GameQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameQuestionEntity
        fields = [
            GameVo.ID,
            GameVo.PRICEABLE,
            GameVo.NUMBER_OF_CHOICES,
            GameVo.PRIORITY,
            GameVo.QUESTION_TEXT,
            GameVo.IS_ACTIVE,
            GameVo.PREDICTION_STARTING_DATE,
            GameVo.PREDICTION_ENDING_DATE,
            GameVo.FINAL_PRICE,
            GameVo.INITIAL_PRICE,
            'choices',
        ]

    choices = RelatedGameChoicesSerializer(many=True, source=GameVo.GAMECHOICESENTITY_SET)
