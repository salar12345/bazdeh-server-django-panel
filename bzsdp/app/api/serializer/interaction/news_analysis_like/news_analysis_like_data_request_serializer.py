from rest_framework import serializers


class NewsAnalysisLikeDataRequestSerializer(serializers.Serializer):
    news_analysis_id = serializers.CharField(max_length=512)
    news_or_analysis = serializers.CharField()

    class Meta:
        fields = ['news_analysis_id', 'news_or_analysis']
