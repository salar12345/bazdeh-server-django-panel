from rest_framework import serializers
from bzsdp.app.model.vo.interaction.inflation_tracker_vo import InflationTrackerVO


class InflationTrackerSerializer(serializers.Serializer):
    priceable_id = serializers.CharField()

    class Meta:
        fields = InflationTrackerVO.__ALL__
