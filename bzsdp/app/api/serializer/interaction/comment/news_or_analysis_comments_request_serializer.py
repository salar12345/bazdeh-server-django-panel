from rest_framework import serializers


class NewsOrAnalysisCommentsRequestSerializer(serializers.Serializer):
    news_or_analysis_id = serializers.CharField()

    class Meta:
        fields = ["news_or_analysis_id"]
