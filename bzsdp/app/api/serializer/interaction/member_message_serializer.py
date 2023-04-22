from rest_framework import serializers


class MemberMessageSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=256)
    content = serializers.CharField(max_length=2048)


    class Meta:
        fields = ['title', 'content']
