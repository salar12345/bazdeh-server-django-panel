from bzscl.model.entity.interaction.risk_measurement_question_entity import RiskMeasurementQuestionEntity
from bzscl.model.vo.interaction.risk_measurement_question_vo import RiskMeasurementQuestionVo
from rest_framework import serializers

from bzsdp.app.api.serializer.interaction.risk_measurement.risk_measurement_choice_serializer import \
    RiskMeasurementChoiceSerializer


class RiskMeasurementQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiskMeasurementQuestionEntity
        fields = [
            RiskMeasurementQuestionVo.ID,
            RiskMeasurementQuestionVo.CONTENT,
            'choices'
        ]

    choices = RiskMeasurementChoiceSerializer(
        source=RiskMeasurementQuestionVo.RISKMEASUREMENTCHOICEENTITY_SET,
        many=True
    )
