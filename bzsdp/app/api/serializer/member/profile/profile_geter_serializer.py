from bzscl.model.entity.member.member_entity import MemberEntity
from rest_framework import serializers


class GetProfileSerializer(serializers.ModelSerializer):
    news_has_been_read_count = serializers.IntegerField()
    analysis_has_been_read_count = serializers.IntegerField()
    risk_measurement_attendance = serializers.BooleanField(allow_null=False, required=True)
    risk_measurement_score = serializers.IntegerField(allow_null=True, required=False)

    class Meta:
        model = MemberEntity
        fields = ["id", "name", "last_name", "phone_number", "image_url", "news_has_been_read_count",
                  "analysis_has_been_read_count", "tag", "risk_measurement_attendance", "risk_measurement_score"]
