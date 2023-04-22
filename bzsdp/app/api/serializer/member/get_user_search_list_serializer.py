from rest_framework import serializers


class Search(serializers.Serializer):
    search = serializers.CharField()
    class Meta:
        fields = ['search']


class GetUserSearchListSerializer(serializers.Serializer):
    search_list = Search(many=True)

    class Meta:
        fields = ['search_list']
