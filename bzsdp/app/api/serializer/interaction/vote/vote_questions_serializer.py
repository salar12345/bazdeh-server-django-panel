from bzscl.model.entity.interaction.vote_questions_entity import VoteQuestionsEntity
from bzscl.model.vo.interaction.vote_questions_vo import VoteQuestionsVo
from rest_framework import serializers

from bzsdp.app.api.serializer.interaction.vote.related_vote_choices_serializer import RelatedVoteChoicesSerializer

class VoteQuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoteQuestionsEntity
        fields = [
            VoteQuestionsVo.ID,
            VoteQuestionsVo.CONTENT,
            VoteQuestionsVo.MULTIPLE_CHOICES,
            'choices'
        ]

    choices = RelatedVoteChoicesSerializer(source='votechoicesentity_set.all', many=True)
