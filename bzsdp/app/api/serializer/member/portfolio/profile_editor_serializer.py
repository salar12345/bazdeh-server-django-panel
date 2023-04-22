from rest_framework import serializers


class ProfileEditorSerializer(serializers.Serializer):
    name = serializers.CharField(allow_blank=True, required=False)
    last_name = serializers.CharField(allow_blank=True, required=False)
    image_url = serializers.CharField(required=False)

    class Meta:
        fields = ['name', 'last_name', 'image_url']


