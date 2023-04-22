from django.db.models import Model
from rest_framework import serializers


class SpecialNewsSerializer(serializers.Serializer):
    category = serializers.CharField(max_length=64)
    page_number = serializers.IntegerField()
    last_news_datetime = serializers.DateTimeField(allow_null=True, required=False)

    class Meta:
        fields = ['category',
                  'page_number',
                  'last_news_datetime']
