from rest_framework import serializers


class EducationSerializer(serializers.Serializer):
    page_number = serializers.IntegerField(max_value=100)
    date_time = serializers.DateTimeField(allow_null=True)

    class Meta:
        fields = ["page_number", "date_time"]
