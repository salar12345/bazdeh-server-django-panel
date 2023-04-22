from rest_framework import serializers
from bzsdp.app.model.vo.interaction.inflation_tracker_vo import InflationTrackerVO


class InflationTrackerDetailSerializer(serializers.Serializer):
    year = serializers.IntegerField()
    price = serializers.FloatField()

    class Meta:
        fields = InflationTrackerVO.__ALL__


class InflationTrackerResultSerializer(serializers.Serializer):
    priceable_name = serializers.CharField()
    unit = serializers.CharField()
    is_default = serializers.BooleanField()
    limit = serializers.IntegerField()
    priceable_info = InflationTrackerDetailSerializer(many=True)

    class Meta:
        fields = InflationTrackerVO.__ALL__
