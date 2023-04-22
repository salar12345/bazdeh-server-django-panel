from rest_framework import serializers


class ProfileImageSerializer(serializers.ModelSerializer):
    image_url = serializers.CharField()

    class Meta:
        exclude = ("image")
