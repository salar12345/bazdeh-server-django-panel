from rest_framework import serializers


class BookmarkSerializer(serializers.Serializer):
    news_id = serializers.CharField(max_length=128)

    class Meta:
        fields = ["news_id"]