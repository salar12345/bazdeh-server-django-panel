from rest_framework import serializers


class WebPostQuerySerializer(serializers.Serializer):
    target_uris = serializers.ListField()
    page_number = serializers.IntegerField()
    category_types = serializers.ListField()
    first_creation_datetime = serializers.CharField(required=False, allow_null=True, allow_blank=False)
