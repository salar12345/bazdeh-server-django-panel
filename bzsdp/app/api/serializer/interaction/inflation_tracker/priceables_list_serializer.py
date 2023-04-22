from rest_framework import serializers
from bzsdp.app.model.vo.interaction.inflation_tracker_vo import InflationTrackerVO


class PriceablesListSerializer(serializers.Serializer):
    priceable_id = serializers.CharField()
    priceable_name = serializers.CharField()
    start_year = serializers.IntegerField()
    end_year = serializers.IntegerField()
    unit = serializers.CharField()
    is_default = serializers.BooleanField()

    class Meta:
        fields = InflationTrackerVO.__ALL__
