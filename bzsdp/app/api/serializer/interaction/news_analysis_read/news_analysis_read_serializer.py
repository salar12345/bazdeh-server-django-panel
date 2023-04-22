from rest_framework import serializers


class NewsAnalysisReadSerializer(serializers.Serializer):
    news_analysis_id = serializers.CharField(max_length=128)
    news_or_analysis = serializers.CharField(max_length=128)

    class Meta:
        fields = ['news_analysis_id', 'news_or_analysis']
