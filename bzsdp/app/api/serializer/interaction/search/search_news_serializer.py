from rest_framework import serializers
from bzsdp.app.model.vo.interaction.search_vo import SearchVo


class SearchNewsSerializer(serializers.Serializer):
    query_string = serializers.CharField()
    page_number = serializers.IntegerField()
    end_datetime = serializers.CharField(required=False)

    class Meta:
        fields = SearchVo.__ALL__
