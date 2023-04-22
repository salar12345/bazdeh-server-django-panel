from bzscl.model.entity.interaction.vote_choices_entity import VoteChoicesEntity
from bzscl.model.vo.interaction.vote_choices_vo import VoteChoicesVo
from rest_framework import serializers


class RelatedVoteChoicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoteChoicesEntity
        fields = [
            VoteChoicesVo.ID,
            VoteChoicesVo.CONTENT
        ]
