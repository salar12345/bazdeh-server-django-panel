from rest_framework import serializers
from bzsdp.app.model.vo.interaction.search_vo import SearchVo


class SearchSerializer(serializers.Serializer):
    query_string = serializers.CharField()
    page_number = serializers.IntegerField()

    class Meta:
        fields = SearchVo.__ALL__
