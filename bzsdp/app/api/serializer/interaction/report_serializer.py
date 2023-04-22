from rest_framework import serializers


class ReportSerializer(serializers.Serializer):
    news_url = serializers.CharField(max_length=256)

    class Meta:
        fields = ['news_url']
