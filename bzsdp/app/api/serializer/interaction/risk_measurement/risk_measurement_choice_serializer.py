from bzscl.model.entity.interaction.risk_measurement_choice_entity import RiskMeasurementChoiceEntity
from bzscl.model.vo.interaction.risk_measurement_choice_vo import RiskMeasurementChoiceVo
from rest_framework import serializers


class RiskMeasurementChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiskMeasurementChoiceEntity
        fields = [RiskMeasurementChoiceVo.ID, RiskMeasurementChoiceVo.CONTENT]
