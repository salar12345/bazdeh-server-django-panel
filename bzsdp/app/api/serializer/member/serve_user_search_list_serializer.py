from rest_framework import serializers


class ServeUserSearchListSerializer(serializers.Serializer):
    query = serializers.CharField()

    class Meta:
        fields = ['query']
