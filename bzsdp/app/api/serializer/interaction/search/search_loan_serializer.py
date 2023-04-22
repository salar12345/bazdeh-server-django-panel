from rest_framework import serializers
from bzsdp.app.model.vo.interaction.search_vo import SearchVo


class SearchLoanSerializer(serializers.Serializer):
    query_string = serializers.CharField()

    class Meta:
        fields = SearchVo.__ALL__
