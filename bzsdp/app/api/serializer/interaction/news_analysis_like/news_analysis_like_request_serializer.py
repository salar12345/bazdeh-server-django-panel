from rest_framework import serializers


class NewsAnalysisLikeRequestSerializer(serializers.Serializer):
    news_analysis_id = serializers.CharField(max_length=128)
    news_or_analysis = serializers.CharField()
    state = serializers.BooleanField(default=True)

    class Meta:
        fields = ['news_analysis_id', 'state', 'news_or_analysis']
