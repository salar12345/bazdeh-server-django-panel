from bzscl.model.entity.interaction.game_choices_entity import GameChoicesEntity
from rest_framework import serializers

from bzsdp.app.model.vo.interaction.game_vo import GameVo


class RelatedGameChoicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameChoicesEntity
        fields = [
            GameVo.ID,
            GameVo.CHOICE_CONTENT,
            GameVo.CHOICE_NUMBER,
            GameVo.VOTERS,
            GameVo.IS_CORRECT
        ]

    voters = serializers.SerializerMethodField()

    def get_voters(self, instance: GameChoicesEntity) -> int:
        return instance.voters.count()
