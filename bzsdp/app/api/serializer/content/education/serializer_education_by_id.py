from rest_framework import serializers


class EducationByIdSerializer(serializers.Serializer):
    education_id = serializers.CharField(max_length=64)

    class Meta:
        fields = ["education_id"]
